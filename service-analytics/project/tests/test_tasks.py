# project/tests/test_routes.py

import json
import time
import datetime as dt

from project import db, create_app
from project.api.models import RepoControlRecord, Commit
from project.tests.base import BaseTestCase
from project.tasks.watcher import task_watcher

app, _ = create_app()

def add_repo(url, coin):
    repo = RepoControlRecord(coin=coin, url=url)
    db.session.add(repo)
    db.session.commit()
    return repo


class TestWatcherClass(BaseTestCase):
    """Tests for the Watcher class"""

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_watcher_class(self):
        add_repo(coin='Test', url='omdv/robinhood-portfolio')
        result = task_watcher()
        self.assertEqual(result, 'Updated 1')

        # time.sleep(2)

        # with app.app_context():
        #     commits = Commit.query.all()
        # self.assertEqual(commits, 42)