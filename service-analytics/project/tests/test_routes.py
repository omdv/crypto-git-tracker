# project/tests/test_routes.py


import json
import time
import pandas as pd
import datetime as dt

from project import db
from project.api.models import Commit
from project.tests.base import BaseTestCase
from concurrent.futures import ThreadPoolExecutor


# helper function to add commits
def add_commit(author, message, type, date):
    commit = Commit(author=author, message=message, type=type, date=date)
    db.session.add(commit)
    db.session.commit()
    return commit


# helper function to mimic long polling
def mimic_polling(delay, tasks):
    print("Started polling")
    result = []
    for i in range(tasks):
        result.append({
            "author": "Poll user {}".format(i),
            "message": "Poll commit {}".format(i),
            "type": "type {}".format(i),
            "date": dt.datetime.today()
            })
        time.sleep(delay)
    df = pd.DataFrame(result)
    return df


# # helper to be called when polling is done
# def polling_done(client, tasks):
#     response = client.get('/commits')
#     data = json.loads(response.data.decode())
#     return len(data['data']['commits'])


class TestAnalyticsService(BaseTestCase):
    """Tests for the Users Service."""

    def test_get_commits(self):
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

    def test_start_polling(self):
        with self.client:
            for delay in [10, 20]:
                response = self.client.post(
                    '/start_poll',
                    data=json.dumps(dict(delay=delay)),
                    content_type='application/json',
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 201)
                self.assertIn(
                    'Polling has started ({}sec)!'.format(delay),
                    data['message'])
                self.assertIn('success', data['status'])

    def test_async_polling(self):
        # mimic_polling(1, 6)
        # response = self.client.get('/commits')
        # data = json.loads(response.data.decode())
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(len(data['data']['commits']), 6)
        
        executor = ThreadPoolExecutor(max_workers=3)

        print("\n")
        delay = 2
        tasks = 5
        future = executor.submit(mimic_polling, delay, tasks)
        # result = future.add_done_callback(polling_done, self.client, tasks)
        # self.assertEqual(result, tasks)
        # self.assertEqual(future.done(), True)

        with self.client:
            print("Started regular updates")
            for i in range(4):
                add_commit(
                    author='Normal user {}'.format(i),
                    message='Normal commit {}'.format(i),
                    type='NA',
                    date=dt.datetime.today()
                )
                response = self.client.get('/commits')
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(data['data']['commits']), i+1)
                time.sleep(2)


        # test after poll is done
        df = future.result()
        df.to_sql(name='commits', con=db.engine, index=False, if_exists="append")
        print("Poll result saved to DB")
        response = self.client.get('/commits')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']['commits']), 4+5)