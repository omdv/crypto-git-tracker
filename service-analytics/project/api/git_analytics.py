import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# define constants
CONTRIBUTOR_COMMITS = 5
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

    """
    Merge series with df under 'name'
    """
    def _merger(self, df, series, name):
        series = series.to_frame()
        series.columns = [name]
        series.reset_index(inplace=True)
        return df.merge(series, on='coin')

    """
    Moving average of daily commits
    """
    def daily_commits_moving_average(self):
        df = self._read_commits()
        df = df.groupby([pd.Grouper(freq='D'), 'coin']).count()['login'].\
            unstack().fillna(0)
        df = df.rolling(DAILY_COMMITS_MA_PERIOD).mean()

        # save to sql
        engine = create_engine(self.DB_URI)
        df.to_sql('daily_commits', engine, index=True, if_exists='replace')
        return df

    """
    Summary table
    """
    def summary_table(self):
        df = self._read_commits()

        # -------------- DEVELOPERS --------------

        # unique developers
        result = df.groupby(['coin']).login.nunique().reset_index()
        result.rename(columns={'login': 'unique_contributors'}, inplace=True)

        # unique contributors
        _c = df.groupby('coin').login.value_counts().unstack().fillna(0).T
        contributors = _c[np.any(_c.values > CONTRIBUTOR_COMMITS, axis=1)]
        count_contrib = contributors.astype(bool).sum(axis=0)
        result = self._merger(result, count_contrib, 'unique_developers')

        # developers MVP
        _df = df.groupby([pd.Grouper(freq='M'), 'coin']).\
            login.value_counts().unstack()
        df_contrib = pd.DataFrame(np.divide(
            _df.values, _df.sum(axis=1).
            values.reshape(-1, 1)), index=_df.index, columns=_df.columns)
        mvps = df_contrib.idxmax(axis=1).unstack().iloc[-2]
        result = self._merger(result, mvps, 'monthly_mvp')

        # ratio of developers to contributors
        result['developers_ratio'] = result['unique_developers']/\
            result['unique_contributors']*100

        # unique developers per day
        unique_devs_day = df.groupby([pd.Grouper(freq='D'), 'coin']).\
            login.nunique().unstack().fillna(0)
        unique_devs_ma = unique_devs_day.rolling(DAILY_DEVS_MA_PERIOD).mean()

        # -------------- COMMITS --------------

        # add commits
        commits = df.groupby(['coin']).message.count().reset_index()
        result = pd.merge(result, commits, how='left', on='coin')
        result.rename(columns={'message': 'number_of_commits'}, inplace=True)

        # commits per day
        commits_per_day = df.groupby([pd.Grouper(freq='D'), 'coin']).\
            count()['login'].unstack().fillna(0)

        # moving average of daily commits
        commits_per_day_rolling = commits_per_day.rolling(
            DAILY_COMMITS_MA_PERIOD).mean()

        # today
        _d1 = commits_per_day_rolling.iloc[-2]
        result = self._merger(result, _d1, 'daily_commits_last')

        # change from day before
        _d2 = commits_per_day_rolling.iloc[-3]
        _d2 = (_d1 - _d2)/_d2 * 100
        result = self._merger(result, _d2, 'daily_commits_change')

        # save to sql
        engine = create_engine(self.DB_URI)
        result.to_sql(
            'summary_table', engine, index=False, if_exists='replace')

        return result, unique_devs_ma


if __name__ == '__main__':
    app_config = {}
    app_config['SQLALCHEMY_DATABASE_URI'] =\
        'postgres://postgres:postgres@localhost:5435/analytics_dev'
    analytics = GitAnalytics(app_config)
    # df = analytics.daily_commits_moving_average()
    d1, d2 = analytics.summary_table()
