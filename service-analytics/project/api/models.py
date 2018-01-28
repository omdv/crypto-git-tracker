# project/api/models.py


from project import db
import datetime as dt

INIT_LAST_UPDATE = dt.datetime(2000, 1, 1)


class Commit(db.Model):
    __tablename__ = "commits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(128), nullable=True)
    message = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    repo = db.Column(db.String(128), nullable=False)
    coin = db.Column(db.String(128), nullable=False)
    symbol = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)

    def __init__(self, login, message, date, repo, coin, symbol, url):
        self.login = login
        self.message = message
        self.date = date
        self.repo = repo
        self.coin = coin
        self.symbol = symbol
        self.url = url


class RepoControlRecord(db.Model):
    __tablename__ = "control_repos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coin = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    symbol = db.Column(db.String(128), nullable=False)
    last_update = db.Column(db.DateTime, nullable=False)

    def __init__(self, coin, symbol, url):
        self.coin = coin
        self.url = url
        self.symbol = symbol
        self.last_update = INIT_LAST_UPDATE
