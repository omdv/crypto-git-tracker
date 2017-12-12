# project/api/views.py
import os
import time

import pandas as pd

from flask import Blueprint, jsonify, request, Response, make_response
from flask import current_app as app

from project import db
from project.api.models import Commit
from project.api.git_watcher import GitWatcher
from project.api.git_analytics import GitAnalytics

from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine

# globals
executor = ThreadPoolExecutor(max_workers=3)
analytics_blueprint = Blueprint('analytics', __name__)
watcher = GitWatcher()

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


@analytics_blueprint.route('/initial_download', methods=['POST'])
def post_initial_download():
    post_data = request.get_json()

    # update configuration of watcher
    watcher.set_app_config(app.config)

    # TEST case
    if post_data:
        if post_data.get('test'):
            watcher.set_page_limit(post_data.get('page_limit'))
            executor.submit(watcher.initial_download)
    # NON TEST CASE
    else:
        watcher.set_page_limit(1000)
        executor.submit(watcher.initial_download)

    response_object = {
        'status': 'success',
        'message': f'Initial download...'
    }
    return jsonify(response_object), 201


@analytics_blueprint.route('/start_poll', methods=['POST'])
def post_start_poll():
    post_data = request.get_json()

    # update configuration of watcher
    watcher.set_app_config(app.config)

    # TEST case
    if post_data:
        if post_data.get('test'):
            watcher.set_page_limit(post_data.get('page_limit'))
            executor.submit(watcher.initial_download)

    # TODO: BUSINESS LOGIC HERE
    # watcher.set_page_limit(3)

    response_object = {
        'status': 'success',
        'message': f'Polling has started!'
    }
    return jsonify(response_object), 201


@analytics_blueprint.route('/stop_poll', methods=['POST'])
def post_stop_poll():
    # update configuration of watcher
    watcher.set_app_config(app.config)

    # stop polling
    watcher.set_polling(False)

    response_object = {
        'status': 'success',
        'message': f'Polling was stopped!'
    }
    return jsonify(response_object), 201


@analytics_blueprint.route('/git_rate_limit', methods=['GET'])
def get_git_rate_limit():

    # update configuration of watcher
    watcher.set_app_config(app.config)

    response_object = {
        'status': 'success',
        'data': {
            'rate_limit': watcher.get_rate_limit()
        }
    }
    return jsonify(response_object), 200


@analytics_blueprint.route('/daily_commits', methods=['GET'])
def get_daily_commits():

    # analytics = GitAnalytics(app.config)
    # _ = analytics.daily_commits_moving_average()

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('daily_commits', engine).fillna(0)

    resp = Response(
        response=df.to_json(orient='records'),
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp