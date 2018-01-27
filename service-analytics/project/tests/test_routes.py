# project/tests/test_routes.py

import json
import time
import datetime as dt

from project import db
from project.api.models import Commit
from project.tests.base import BaseTestCase


# helper function to add commits
def add_commit(author, message, date, delay=0):
    commit = Commit(author=author, message=message, date=date)
    db.session.add(commit)
    db.session.commit()
    time.sleep(delay)
    return commit


# class TestAnalyticsService(BaseTestCase):
#     """Tests for the Analytics Service."""

#     def test_get_commits(self):
#         add_commit(
#             author='michael',
#             message='Test #1',
#             date=dt.datetime.today())
#         add_commit(
#             author='jerry',
#             message='Test #2',
#             date=dt.datetime.today())
#         with self.client:
#             response = self.client.get('/commits')
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(len(data['data']['commits']), 2)
#             self.assertTrue('date' in data['data']['commits'][0])
#             self.assertTrue('date' in data['data']['commits'][1])
#             self.assertIn('michael', data['data']['commits'][0]['author'])
#             self.assertIn('Test #1', data['data']['commits'][0]['message'])
#             self.assertIn('jerry', data['data']['commits'][1]['author'])
#             self.assertIn('Test #2', data['data']['commits'][1]['message'])
#             self.assertIn('success', data['status'])
#             self.assertIn('success', data['status'])



