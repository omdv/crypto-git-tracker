# project/api/views.py
import os
import time

import pandas as pd

from flask import Blueprint, jsonify, request
from flask import current_app as app

from project import db
from project.api.models import Commit
from project.api.git_poller import GitPoller

from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine

# globals
executor = ThreadPoolExecutor(max_workers=3)
analytics_blueprint = Blueprint('analytics', __name__)

# helper for testing polling api
def long_function(delay):
    time.sleep(delay*1.5)


@analytics_blueprint.route('/commits', methods=['GET'])
def get_all_commits():
    """Get all commits"""
    # commits = Commit.query.all()
    # commits_list = []
    # for commit in commits:
    #     commit_object = {
    #         'id': commit.id,
    #         'author': commit.author,
    #         'message': commit.message,
    #         'type': commit.type,
    #         'date': commit.date
    #     }
    #     commits_list.append(commit_object)
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('commits', engine)
    response_object = {
        'status': 'success',
        'data': {
            'commits': df.to_dict(orient='records')
        }
    }
    return jsonify(response_object), 200


@analytics_blueprint.route('/start_poll', methods=['POST'])
def post_start_poll():
    post_data = request.get_json()

    # instantiate poller
    poller = GitPoller(app.config)

    # TEST case
    if post_data.get('test'):
        poller.set_page_limit(post_data.get('page_limit'))
        executor.submit(poller.initial_download, 'commits')

    # TODO: BUSINESS LOGIC HERE
    # poller.set_page_limit(3)

    response_object = {
        'status': 'success',
        'message': f'Polling has started!'
    }
    return jsonify(response_object), 201


@analytics_blueprint.route('/git_rate_limit', methods=['GET'])
def get_git_rate_limit():

    # instantiate poller
    poller = GitPoller(app.config)

    response_object = {
        'status': 'success',
        'data': {
            'rate_limit': poller.get_rate_limit
        }
    }
    return jsonify(response_object), 200
