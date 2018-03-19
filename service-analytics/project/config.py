# project/config.py

import os
from datetime import timedelta


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GIT_USER = os.environ.get('GIT_USER')
    GIT_TOKEN = os.environ.get('GIT_TOKEN')

    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_BACKEND_URL = 'redis://redis:6379/0'
    CELERY_TIMEZONE = 'UTC'
    ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': 'redis://redis:6379/0',
            'default_timeout': 60 * 60
        }
    }


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TIME_DELTA = 120
    CELERYBEAT_SCHEDULE = {
        'watcher': {
            'task': 'task_watcher',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'summary': {
            'task': 'task_summary',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'rate_limit': {
            'task': 'task_rate_limit',
            'schedule': timedelta(seconds=TIME_DELTA)
        }
    }


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    TIME_DELTA = 10
    CELERYBEAT_SCHEDULE = {
        'watcher': {
            'task': 'task_watcher',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'summary': {
            'task': 'task_summary',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'rate_limit': {
            'task': 'task_rate_limit',
            'schedule': timedelta(seconds=TIME_DELTA)
        }
    }


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    TIME_DELTA = 180
    CELERYBEAT_SCHEDULE = {
        'watcher': {
            'task': 'task_watcher',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'summary': {
            'task': 'task_summary',
            'schedule': timedelta(seconds=TIME_DELTA)
        },
        'rate_limit': {
            'task': 'task_rate_limit',
            'schedule': timedelta(seconds=TIME_DELTA)
        }
    }