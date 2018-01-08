# project/config.py

import os
import json


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