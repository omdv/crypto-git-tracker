# project/tests/test_tasks.py

import json
from project import db
from project.api.models import RepoControlRecord, Commit
from project.tests.base import BaseTestCase
from project.analytics.git_watcher import GitWatcher
from project.analytics.git_analytics import GitAnalytics
from flask import current_app


def add_repo(ticker, apihandle, url):
    repo = RepoControlRecord(ticker=ticker,
                             apihandle=apihandle, url=url)
    db.session.add(repo)
    db.session.commit()
    return repo


def call_watcher_task(repos):
    updated = 0
    for repo in repos:
        watcher = GitWatcher(repo.ticker, repo.apihandle,
                             repo.url, repo.last_update)
        watcher.set_app_config(current_app.config)
        new_date = watcher.download()
        if new_date:
            repo.last_update = new_date
            updated += 1
        db.session.add(repo)
    db.session.commit()
    return "Updated {} of {}".format(updated, len(repos))


def call_summary_task(app_config):
    analyzer = GitAnalytics(app_config)
    df, _, _ = analyzer.summary_table()
    return df


class TestCeleryTasksClass(BaseTestCase):
    """Tests for the Watcher class"""

    def test_celery_tasks(self):
        add_repo(ticker='BTC', apihandle='bitcoin',
                 url='omdv/robinhood-portfolio')
        add_repo(ticker='ETH', apihandle='ethereum',
                 url='omdv/openai-gym-agents')
        repos = RepoControlRecord.query.all()
        self.assertEqual(len(repos), 2)

        # first call
        result = call_watcher_task(repos)
        self.assertEqual(result, 'Updated 2 of 2')
        commits = Commit.query.all()
        self.assertEqual(len(commits), 56)

        # second call
        repos = RepoControlRecord.query.all()
        result = call_watcher_task(repos)
        self.assertEqual(result, 'Updated 0 of 2')
        commits = Commit.query.all()
        self.assertEqual(len(commits), 56)

        # call summary
        df = call_summary_task(current_app.config)
        self.assertIn('omdv', df['monthly_mvp'].values)
        self.assertEqual(100, df['developers_ratio'].values[0])

        with self.client:
            response = self.client.get('/all_commits')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 56)

            response = self.client.get('/commits')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 65)

            response = self.client.get('/developers')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 65)

            response = self.client.get('/summary_table')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            self.assertIn('omdv', data[0]['monthly_mvp'])
