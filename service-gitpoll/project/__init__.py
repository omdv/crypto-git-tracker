# service-analytics/project/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# instantiate the app
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)


# model
class Commits(db.Model):
    __tablename__ = "commits"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(128), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __init__(self, author, message, type, date):
        self.author = author
        self.message = message
        self.type = type
        self.date = date
