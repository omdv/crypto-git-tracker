# project/api/views.py
import pandas as pd

from flask import Blueprint, Response, jsonify
from flask import current_app as app
from project.analytics.git_watcher import GitWatcher

from sqlalchemy import create_engine

# globals
db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/commits', methods=['GET'])
def get_all_commits():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('commits', engine)
    response_object = {
        'status': 'success',
        'data': {
            'commits': df.to_dict(orient='records')
        }
    }
    return jsonify(response_object), 200


@db_blueprint.route('/daily_commits', methods=['GET'])
def get_daily_commits():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('daily_commits', engine).fillna(0)
    # df.set_index('date', inplace=True)

    resp = Response(
        response=df.to_json(orient='records'),
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@db_blueprint.route('/daily_devs', methods=['GET'])
def get_daily_devs():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('daily_devs', engine).fillna(0)
    df.set_index('date', inplace=True)

    resp = Response(
        response=df.to_json(orient='records'),
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@db_blueprint.route('/summary_table', methods=['GET'])
def get_summary_table():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    df = pd.read_sql('summary_table', engine)

    resp = Response(
        response=df.to_json(orient='records'),
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@db_blueprint.route('/test', methods=['GET'])
def test_db():
    return "test passed", 200


@db_blueprint.route('/git_rate_limit', methods=['GET'])
def get_git_rate_limit():

    # update configuration of watcher
    watcher = GitWatcher(None, None, None, None)
    watcher.set_app_config(app.config)

    response_object = {
        'status': 'success',
        'data': {
            'rate_limit': watcher.get_rate_limit()
        }
    }
    return jsonify(response_object), 200
