# project/tests/test_routes.py

# import os
import json
import time
# import pandas as pd
import datetime as dt

from project import db
from project.api.models import Commit
from project.tests.base import BaseTestCase
# from concurrent.futures import ThreadPoolExecutor
# from sqlalchemy import create_engine

# executor = ThreadPoolExecutor(max_workers=3)


# helper function to add commits
def add_commit(author, message, date, delay=0):
    commit = Commit(author=author, message=message, date=date)
    db.session.add(commit)
    db.session.commit()
    time.sleep(delay)
    return commit


# # helper function to mimic long polling
# def mimic_polling(delay, tasks):
#     print("Started polling")
#     result = []
#     for i in range(tasks):
#         result.append({
#             "author": "Poll user {}".format(i),
#             "message": "Poll commit {}".format(i),
#             "type": "type {}".format(i),
#             "date": dt.datetime.today()
#             })
#         print("Completed poll {}".format(i))
#         time.sleep(delay)
#     df = pd.DataFrame(result)
#     engine = create_engine(os.environ.get('DATABASE_TEST_URL'))
#     df.to_sql(name='commits', con=engine, index=False, if_exists="append")
#     print("Poll results saved to DB")
#     return df


class TestAnalyticsService(BaseTestCase):
    """Tests for the Analytics Service."""

    def test_get_commits(self):
        add_commit(
            author='michael',
            message='Test #1',
            date=dt.datetime.today())
        add_commit(
            author='jerry',
            message='Test #2',
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
            self.assertIn('success', data['status'])

    def test_start_polling(self):
        with self.client:
            for page_limit in [1, 2]:
                response = self.client.post(
                    '/start_poll',
                    data=json.dumps(dict(test=True, page_limit=page_limit)),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn('Polling has started!', data['message'])
                self.assertIn('success', data['status'])
                time.sleep(3)
                response = self.client.get('/commits')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(data['data']['commits']), page_limit*100)


    # def test_polling(self):
    #     print("\n")
    #     delay = 1
    #     tasks = 3

    #     future = executor.submit(mimic_polling, delay, tasks)

    #     with self.client:
    #         print("Start normal commits")
    #         for i in range(tasks):
    #             add_commit(
    #                 author='Normal user {}'.format(i),
    #                 message='Normal commit {}'.format(i),
    #                 type='NA',
    #                 date=dt.datetime.today()
    #             )
    #             response = self.client.get('/commits')
    #             data = json.loads(response.data.decode())
    #             self.assertEqual(response.status_code, 200)
    #             time.sleep(.5)
    #             print("Completed normal commit {}".format(i))

    #     future.result()
    #     response = self.client.get('/commits')
    #     data = json.loads(response.data.decode())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(data['data']['commits']), tasks*2)