# project/config.py

import os
import json


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    GIT_REPOS = {
        'BTC': ['bitcoin/bitcoin'],
        'ETH': ['ethereum/go-ethereum'],
        'BCH': [
            'Bitcoin-ABC/bitcoin-abc',
            'bitcoinclassic/bitcoinclassic',
            'bitcoinxt/bitcoinxt',
            'BitcoinUnlimited/BitcoinUnlimited'],
        'ADA': ['input-output-hk/cardano-sl']}


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # GIT_SECRET = json.load(open('/run/secrets/my_git_secret'))
    GIT_SECRET = {'USER': 'omdv', 'TOKEN': 'bdbae9884072bba932f755ee370fd85f001a2928'}


class TestingConfig(BaseConfig):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    # GIT_SECRET = json.load(open('/run/secrets/my_git_secret'))
    GIT_SECRET = {'USER': 'omdv', 'TOKEN': 'bdbae9884072bba932f755ee370fd85f001a2928'}
    GIT_REPOS = {'BTC': ['bitcoin/bitcoin']}


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # GIT_SECRET = json.load(open('/run/secrets/my_git_secret'))
    GIT_SECRET = {'USER': 'omdv', 'TOKEN': 'bdbae9884072bba932f755ee370fd85f001a2928'}