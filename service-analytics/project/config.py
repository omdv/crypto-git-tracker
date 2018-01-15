# project/config.py

import os
import json
from datetime import timedelta


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GIT_REPOS = {
        'BTC': ['bitcoin/bitcoin'],
        'ETH': ['ethereum/go-ethereum'],
        'BCH': [
            'Bitcoin-ABC/bitcoin-abc',
            'bitcoinclassic/bitcoinclassic',
            'bitcoinxt/bitcoinxt',
            'BitcoinUnlimited/BitcoinUnlimited'],
        'ADA': ['input-output-hk/cardano-sl']}
    GIT_USER = os.environ.get('GIT_USER')
    GIT_TOKEN = os.environ.get('GIT_TOKEN')

    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_BACKEND_URL = 'redis://redis:6379/0'
    CELERY_TIMEZONE = 'UTC'
    CELERYBEAT_SCHEDULE = {
        'say-every-5-seconds': {
            'task': 'test_watcher',
            'schedule': timedelta(seconds=5)
        },
        'say-every-10-seconds': {
            'task': 'test_summary',
            'schedule': timedelta(seconds=10)
        },
    }



class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    GIT_REPOS = {'BTC': ['bitcoin/bitcoin']}


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')