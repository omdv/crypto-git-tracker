import requests
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# define constants
DEVELOPER_COMMITS = 5
DAILY_COMMITS_MA_PERIOD = 10
DAILY_DEVS_MA_PERIOD = 10


class GitAnalytics():
    def __init__(self, app_config):
        self.DB_URI = app_config['SQLALCHEMY_DATABASE_URI']

    def _read_commits(self):
        engine = create_engine(self.DB_URI)
        df = pd.read_sql('commits', engine)
        df.set_index("date", inplace=True)
        return df

    def _download_market_info(self, coin):
        url = 'https://api.coinmarketcap.com/v1/ticker/{}/'.format(coin)
        _r = requests.get(url)
        try:
            _d = _r.json()[0]
        except KeyError:
            _d = {'price_usd': 0, 'market_cap_usd': 0}
        return float(_d['price_usd']), float(_d['market_cap_usd'])

    """
    Merge series with df under 'name'
    """
    def _merger(self, df, series, name):
        series = series.to_frame()
        series.columns = [name]
        series.reset_index(inplace=True)
        return df.merge(series, on='coin')

    """
    Main function
    Generates three tables in DB
    """
    def summary_table(self):
        df = self._read_commits()
        engine = create_engine(self.DB_URI)

        # -------------- DEVELOPERS --------------
        # unique contributors
        result = df.groupby(['coin']).login.nunique().reset_index()
        result.rename(columns={'login': 'unique_contributors'}, inplace=True)

        # unique developers > N commits
        _c = df.groupby('coin').login.value_counts().unstack().fillna(0).T
        _devs = _c[np.any(_c.values > DEVELOPER_COMMITS, axis=1)]
        _devs = _devs.astype(bool).sum(axis=0)
        result = self._merger(result, _devs, 'unique_developers')

        # developers MVP
        _df = df.groupby([pd.Grouper(freq='M'), 'coin']).\
            login.value_counts().unstack()
        df_contrib = pd.DataFrame(np.divide(
            _df.values, _df.sum(axis=1).
            values.reshape(-1, 1)), index=_df.index, columns=_df.columns)
        mvps = df_contrib.idxmax(axis=1).unstack().iloc[-2]
        result = self._merger(result, mvps, 'monthly_mvp')

        # ratio of developers to contributors
        result['developers_ratio'] = result['unique_developers'] /\
            result['unique_contributors'] * 100

        # unique developers per day
        unique_devs = df.groupby([pd.Grouper(freq='D'), 'coin']).\
            login.nunique().unstack().fillna(0)

        # resample to 1 day and produce MA
        unique_devs = unique_devs.resample('1D').asfreq().fillna(0)
        unique_devs_ma = unique_devs.rolling(DAILY_DEVS_MA_PERIOD).mean()

        # today
        _d1 = unique_devs_ma.iloc[-2]
        result = self._merger(result, _d1, 'today_devs')

        # change from day before
        _d2 = unique_devs_ma.iloc[-3]
        _d2 = (_d1 - _d2) / _d2 * 100
        # fix division by zero
        _d2.fillna(0, inplace=True)
        result = self._merger(result, _d2, 'today_devs_change')


        # -------------- COMMITS --------------
        # add commits
        commits = df.groupby(['coin']).message.count().reset_index()
        result = pd.merge(result, commits, how='left', on='coin')
        result.rename(columns={'message': 'number_of_commits'}, inplace=True)

        # commits per day
        commits_day = df.groupby([pd.Grouper(freq='D'), 'coin']).\
            count()['login'].unstack().fillna(0)

        # resample to 1 day and produce MA
        commits_day = commits_day.resample('1D').asfreq().fillna(0)
        commits_day_ma = commits_day.rolling(
            DAILY_COMMITS_MA_PERIOD).mean()

        # today
        _d1 = commits_day_ma.iloc[-2]
        result = self._merger(result, _d1, 'today_commits')

        # change from day before
        _d2 = commits_day_ma.iloc[-3]
        _d2 = (_d1 - _d2) / _d2 * 100
        # fix division by zero
        _d2.fillna(0, inplace=True)
        result = self._merger(result, _d2, 'today_commits_change')

        # -------------- MARKET DATA --------------
        result[['price', 'market_cap']] = result['coin'].\
            apply(self._download_market_info).\
            apply(pd.Series)

        # -------------- REPOS DATA --------------
        _rc = df.groupby(['coin']).repo.nunique().reset_index()
        _rc.rename(columns={'repo': 'repo_count'}, inplace=True)
        result = pd.merge(result, _rc, how='left', on='coin')

        # unique repos
        _rp = df.groupby('coin').repo.apply(pd.unique).reset_index()
        _rp.rename(columns={'repo': 'repos'}, inplace=True)
        _rp['repos'] = _rp['repos'].apply(",".join)
        result = pd.merge(result, _rp, how='left', on='coin')

        # -------------- SQL --------------
        commits_day_ma.reset_index(inplace=True)
        commits_day_ma.to_sql(
            'daily_commits', engine, index=False, if_exists='replace')

        unique_devs_ma.reset_index(inplace=True)
        unique_devs_ma.to_sql(
            'daily_devs', engine, index=False, if_exists='replace')

        result.to_sql(
            'summary_table', engine, index=False, if_exists='replace')

        return result, commits_day_ma, unique_devs_ma


if __name__ == '__main__':
    app_config = {}
    app_config['SQLALCHEMY_DATABASE_URI'] =\
        'postgres://postgres:postgres@localhost:5435/analytics_dev'
    an = GitAnalytics(app_config)
    d1, d2, d3 = an.summary_table()
