# project/tests/test_config.py


import unittest
import os
import json

from flask import current_app
from flask_testing import TestCase

from project import create_app
app = create_app()


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )
        # self.assertTrue(
        #     app.config['GIT_SECRET'] ==
        #     json.load(open("/run/secrets/my_git_secret"))
        # )
        for key in ['SECRET_KEY']:
            self.assertTrue(
                app.config[key] ==
                os.environ.get(key))


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        for key in ['SECRET_KEY']:
            self.assertTrue(
                app.config[key] ==
                os.environ.get(key))
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )
        # self.assertTrue(
        #     app.config['GIT_SECRET'] ==
        #     json.load(open("/run/secrets/my_git_secret"))
        # )
        self.assertTrue(
            app.config['GIT_REPOS'] == {'BTC': ['bitcoin/bitcoin']}
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        for key in ['SECRET_KEY']:
            self.assertTrue(
                app.config[key] ==
                os.environ.get(key))
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        # self.assertTrue(
        #     app.config['GIT_SECRET'] ==
        #     json.load(open("/run/secrets/my_git_secret"))
        # )


if __name__ == '__main__':
    unittest.main()
