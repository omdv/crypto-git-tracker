# project/tests/test_routes.py


import json
import datetime as dt

from project import db
from project.api.models import Commit
from project.tests.base import BaseTestCase


def add_commit(author, message, type, date):
    commit = Commit(author=author, message=message, type=type, date=date)
    db.session.add(commit)
    db.session.commit()
    return commit


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_get_commits(self):
        """Ensure the /commits route behaves correctly."""
        add_commit(
            author='michael',
            message='Test #1',
            type='doc',
            date=dt.datetime.today())
        add_commit(
            author='jerry',
            message='Test #2',
            type='algo',
            date=dt.datetime.today())
        with self.client:
            response = self.client.get('/commits')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['commits']), 2)
            self.assertTrue('date' in data['data']['commits'][0])
            self.assertTrue('date' in data['data']['commits'][1])
            self.assertIn('michael', data['data']['commits'][0]['author'])
            self.assertIn('Test #1', data['data']['commits'][0]['message'])
            self.assertIn('jerry', data['data']['commits'][1]['author'])
            self.assertIn('Test #2', data['data']['commits'][1]['message'])
            self.assertIn('success', data['status'])
            self.assertIn('doc', data['data']['commits'][0]['type'])
            self.assertIn('algo', data['data']['commits'][1]['type'])
            self.assertIn('success', data['status'])

