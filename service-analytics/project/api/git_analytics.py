import pandas as pd
from sqlalchemy import create_engine


class GitAnalytics():
    def __init__(self, app_config):
        self.DB_URI = app_config['SQLALCHEMY_DATABASE_URI']

    def _read_commits(self):
        engine = create_engine(self.DB_URI)
        df = pd.read_sql('commits', engine)
        df.set_index("date", inplace=True)
        return df

    """
    Moving average of daily commits
    """
    def daily_commits_moving_average(self, period=30):
        df = self._read_commits()
        print(df.info())
        df = df.groupby([pd.Grouper(freq='D'), 'coin']).count()['login'].unstack().fillna(0)
        df = df.rolling(period).mean()
        engine = create_engine(self.DB_URI)
        df.to_sql('daily_commits', engine, index=True, if_exists='replace')
        return df

if __name__ == '__main__':
    app_config = {}
    app_config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:postgres@localhost:5435/analytics_dev'
    analytics = GitAnalytics(app_config)
    df = analytics.daily_commits_moving_average()

