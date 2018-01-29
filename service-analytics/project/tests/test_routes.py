# project/tests/test_routes.py

import json
import time
import datetime as dt

from project import db
from project.api.models import Commit
from project.tests.base import BaseTestCase


# helper function to add commits
def add_commit(login, message, date, repo,
               ticker, apihandle, url, delay=0):
    commit = Commit(
        login=login, message=message, date=date, repo=repo, ticker=ticker,
        apihandle=apihandle, url=url)
    db.session.add(commit)
    db.session.commit()
    time.sleep(delay)
    return commit


class TestAnalyticsService(BaseTestCase):
    """Tests for the Analytics Service."""

    def test_get_commits(self):
        add_commit(
            login='michael',
            message='Test #1',
            date=dt.datetime.today(),
            ticker='BTC',
            apihandle='bitcoin',
            repo='repo/repo',
            url='url')
        add_commit(
            login='jerry',
            message='Test #2',
            date=dt.datetime.today(),
            ticker='ETH',
            apihandle='ethereum',
            repo='repo/repo',
            url='url')
        with self.client:
            response = self.client.get('/commits')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['commits']), 2)
            self.assertTrue('date' in data['data']['commits'][0])
            self.assertTrue('date' in data['data']['commits'][1])
            self.assertIn('michael', data['data']['commits'][0]['login'])
            self.assertIn('Test #1', data['data']['commits'][0]['message'])
            self.assertIn('jerry', data['data']['commits'][1]['login'])
            self.assertIn('Test #2', data['data']['commits'][1]['message'])
            self.assertIn('success', data['status'])
            self.assertIn('success', data['status'])
