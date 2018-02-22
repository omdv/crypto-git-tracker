# project/api/views.py
import pandas as pd

from flask import Blueprint, Response, jsonify
from flask import current_app as app

from sqlalchemy import create_engine

# globals
db_blueprint = Blueprint('db', __name__)


@db_blueprint.route('/all_commits', methods=['GET'])
def get_all_commits():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        df = pd.read_sql('commits', engine)
        resp = Response(
            response=df.to_json(orient='records'),
            status=200,
            mimetype="application/json")

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)


@db_blueprint.route('/commits', methods=['GET'])
def get_daily_commits():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        df = pd.read_sql('daily_commits', engine).fillna(0)
        resp = Response(
            response=df.to_json(orient='records'),
            status=200,
            mimetype="application/json")

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)


@db_blueprint.route('/developers', methods=['GET'])
def get_daily_devs():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        df = pd.read_sql('daily_devs', engine).fillna(0)
        resp = Response(
            response=df.to_json(orient='records'),
            status=200,
            mimetype="application/json")
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)


@db_blueprint.route('/summary_table', methods=['GET'])
def get_summary_table():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        df = pd.read_sql('summary_table', engine)
        resp = Response(
            response=df.to_json(orient='records'),
            status=200,
            mimetype="application/json")

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)


@db_blueprint.route('/test', methods=['GET'])
def test_db():
    return "test passed", 200


@db_blueprint.route('/git_rate_limit', methods=['GET'])
def get_git_rate_limit():
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        df = pd.read_sql('git_rate_limit', engine)
        df = df[['time', 'rate']]
        # df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        resp = Response(
            response=df.to_json(orient='records'),
            status=200,
            mimetype="application/json")

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)
