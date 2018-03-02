# project/api/models.py


from project import db
import datetime as dt

INIT_LAST_UPDATE = dt.datetime(2000, 1, 1)


class Commit(db.Model):
    __tablename__ = "commits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), nullable=True)
    message = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    repo = db.Column(db.String(64), nullable=False)
    ticker = db.Column(db.String(16), nullable=False)
    apihandle = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(256), nullable=False)

    def __init__(self, login, message, date, repo, ticker, apihandle, url):
        self.login = login
        self.message = message
        self.date = date
        self.repo = repo
        self.ticker = ticker
        self.apihandle = apihandle
        self.url = url


class RepoControlRecord(db.Model):
    __tablename__ = "control_repos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticker = db.Column(db.String(16), nullable=False)
    apihandle = db.Column(db.String(64), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)

    def __init__(self, ticker, apihandle, url):
        self.ticker = ticker
        self.apihandle = apihandle
        self.url = url
        self.last_update = INIT_LAST_UPDATE


class GitRateLimitModel(db.Model):
    __tablename__ = "git_rate_limit"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=False)
    rate = db.Column(db.Integer, nullable=False)

    def __init__(self, time, rate):
        self.time = time
        self.rate = rate
