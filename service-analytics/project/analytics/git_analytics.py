import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# define constants
DEVELOPER_COMMITS = 5
DAILY_COMMITS_MA_PERIOD = 16
DAILY_DEVS_MA_PERIOD = 16


class GitAnalytics():
    def __init__(self, app_config):
        self.DB_URI = app_config['SQLALCHEMY_DATABASE_URI']

    def _read_commits(self):
        engine = create_engine(self.DB_URI)
        df = pd.read_sql('commits', engine)
        df.drop_duplicates(
            subset=['ticker', 'login', 'date', 'message', 'url'], inplace=True)
        df.set_index("date", inplace=True)
        return df

    def _download_market_info(self, apihandle):
        url = 'https://api.coinmarketcap.com/v1/ticker/{}/'.format(apihandle)
        # print('Downloading market info for {}'.format(apihandle))
        _r = requests.get(url)
        try:
            _d = _r.json()[0]
            return float(_d['price_usd']),\
                float(_d['market_cap_usd']) / 1.e6, _d['name']
        except KeyError:
            print('Problem parsing {}'.format(apihandle))
            return 0, 0, 'ERROR'

    """
    Merge series with df under 'name'
    """
    def _merger(self, df, series, name):
        series = series.to_frame()
        series.columns = [name]
        series.reset_index(inplace=True)
        return df.merge(series, on='ticker')

    """
    Main function
    Generates three tables in DB
    """
    def summary_table(self):
        df = self._read_commits()
        engine = create_engine(self.DB_URI)

        # return none if dataframe is empty
        if df.shape[0] == 0:
            return None, None, None

        # -------------- DEVELOPERS --------------
        # unique contributors
        result = df.groupby(['ticker', 'apihandle']).\
            login.nunique().reset_index()
        result.rename(columns={'login': 'unique_contributors'}, inplace=True)

        # unique developers > N commits
        _c = df.groupby('ticker').login.value_counts().unstack().fillna(0).T
        _devs = _c[np.any(_c.values > DEVELOPER_COMMITS, axis=1)]
        _devs = _devs.astype(bool).sum(axis=0)
        result = self._merger(result, _devs, 'unique_developers')

        # developers MVP
        _df = df.groupby([pd.Grouper(freq='M'), 'ticker']).\
            login.value_counts().unstack()
        df_contrib = pd.DataFrame(np.divide(
            _df.values, _df.sum(axis=1).
            values.reshape(-1, 1)), index=_df.index, columns=_df.columns)
        mvps = df_contrib.idxmax(axis=1).unstack().iloc[-2]
        result = self._merger(result, mvps, 'monthly_mvp')

        # ratio of developers to contributors
        result['developers_ratio'] = result['unique_developers'] /\
            result['unique_contributors'] * 100

        # unique developers per period
        unique_devs = df.groupby([pd.Grouper(freq='W'), 'ticker']).\
            login.nunique().unstack().fillna(0)

        # resample and produce MA
        unique_devs = unique_devs.resample('1W').asfreq().fillna(0)
        unique_devs_ma = unique_devs.rolling(DAILY_DEVS_MA_PERIOD).mean()

        # get maximum activity values and current activity
        unique_devs_mean = unique_devs.mean(axis=1)
        unique_devs_max_date = unique_devs_mean.idxmax()
        unique_devs_current =\
            unique_devs_mean.iloc[-1] / unique_devs_mean.max() * 100
        hours_passed =\
            (pd.datetime.today() - unique_devs_mean.index[-2]) /\
            np.timedelta64(1, 'h') / 168
        # normalize by number of elapsed hours
        unique_devs_current /= hours_passed

        # add days since the launch
        _launch_date = unique_devs.apply(
            lambda x: pd.Timestamp.now() - x[x != 0].index[0], axis=0)
        result = self._merger(result, _launch_date, 'days_since_launch')
        result['days_since_launch'] = result['days_since_launch'].apply(
            lambda x: x.days)

        # mean number of devs per period since launch
        _mean_devs_period = unique_devs.apply(
            lambda x: x[x[x != 0].index[0]:].mean(), axis=0)
        result = self._merger(result, _mean_devs_period, 'mean_devs_period')

        # -------------- COMMITS --------------
        # add commits
        commits = df.groupby(['ticker']).message.count().reset_index()
        result = pd.merge(result, commits, how='left', on='ticker')
        result.rename(columns={'message': 'number_of_commits'}, inplace=True)

        # dropping similar commits for the same coin
        df.drop_duplicates(subset=['ticker', 'login', 'date', 'message'],
                           inplace=True)

        # commits per day
        commits_day = df.groupby([pd.Grouper(freq='W'), 'ticker']).\
            count()['login'].unstack().fillna(0)

        # resample and produce MA
        commits_day = commits_day.resample('1W').asfreq().fillna(0)
        commits_day_ma = commits_day.rolling(
            DAILY_COMMITS_MA_PERIOD).mean()

        # get maximum activity values and current activity
        commits_mean = commits_day.mean(axis=1)
        commits_max_date = commits_mean.idxmax()
        commits_current =\
            commits_mean.iloc[-1] / commits_mean.max() * 100
        # normalize by number of elapsed hours
        commits_current /= hours_passed

        # mean number of commits per period since launch
        _mean_commits_day = commits_day.apply(
            lambda x: x[x[x != 0].index[0]:].mean(), axis=0)
        result = self._merger(result, _mean_commits_day, 'mean_commits_period')

        # -------------- MARKET DATA --------------
        result[['price', 'market_cap', 'name']] = result['apihandle'].\
            apply(self._download_market_info).\
            apply(pd.Series)

        # normalized data
        result['avg_commits_per_market_cap'] =\
            result['mean_commits_period'] / result['market_cap'] * 1000

        result['avg_devs_per_market_cap'] =\
            result['mean_devs_period'] / result['market_cap'] * 1000

        # -------------- REPOS DATA --------------
        _rc = df.groupby(['ticker']).repo.nunique().reset_index()
        _rc.rename(columns={'repo': 'repo_count'}, inplace=True)
        # result = pd.merge(result, _rc, how='left', on='ticker')

        # unique repos
        _rp = df.groupby('ticker').repo.apply(pd.unique).reset_index()
        _rp.rename(columns={'repo': 'repos'}, inplace=True)
        _rp['repos'] = _rp['repos'].apply(",".join)
        result = pd.merge(result, _rp, how='left', on='ticker')

        X = result['avg_commits_per_market_cap'].values
        result['commits_ratio_90'] = (X > np.percentile(X, 90)).astype('int')
        result['commits_ratio_10'] = (X < np.percentile(X, 10)).astype('int')

        X = result['avg_devs_per_market_cap'].values
        result['devs_ratio_90'] = (X > np.percentile(X, 90)).astype('int')
        result['devs_ratio_10'] = (X < np.percentile(X, 10)).astype('int')

        # -------------- SQL --------------
        commits_day_ma.reset_index(inplace=True)
        commits_day_ma.to_sql(
            'daily_commits', engine, index=False, if_exists='replace')

        unique_devs_ma.reset_index(inplace=True)
        unique_devs_ma.to_sql(
            'daily_devs', engine, index=False, if_exists='replace')

        result.to_sql(
            'summary_table', engine, index=False, if_exists='replace')

        activity_levels = pd.DataFrame({
            'max_commits_date': [commits_max_date],
            'current_commits_level': [commits_current],
            'max_devs_date': [unique_devs_max_date],
            'current_devs_level': [unique_devs_current]})
        activity_levels.to_sql(
            'activity_levels', engine, index=False, if_exists='replace')

        return result, commits_day_ma, unique_devs_ma, activity_levels


if __name__ == '__main__':
    app_config = {}
    app_config['SQLALCHEMY_DATABASE_URI'] =\
        'postgres://postgres:postgres@192.168.99.104:5432/analytics_dev'
    an = GitAnalytics(app_config)
    d1, d2, d3, d4 = an.summary_table()
