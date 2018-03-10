# project/api/views.py
import datetime as dt
from json import dumps
from decimal import Decimal
from flask import Blueprint, Response
from flask import current_app as app

from sqlalchemy import create_engine, text

# globals
db_blueprint = Blueprint('db', __name__)


def alchemy_encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, dt.date):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)


def form_response(sql_query):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    try:
        query = text(sql_query)
        res = engine.execute(query)
        res = dumps([dict(r) for r in res], default=alchemy_encoder)

        resp = Response(
            response=res,
            status=200,
            mimetype="application/json")

        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except:
        return Response(response=None, status=400)


@db_blueprint.route('/hello', methods=['GET'])
def get_hello():
    resp = Response(
        response="Hello World!",
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@db_blueprint.route('/test', methods=['GET'])
def test_db():
    resp = Response(
        response="test passed",
        status=200,
        mimetype="application/json")

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@db_blueprint.route('/control_repos', methods=['GET'])
def get_control_repos():
    query = "SELECT * FROM control_repos"
    return form_response(query)


@db_blueprint.route('/all_commits', methods=['GET'])
def get_all_commits():
    query = "SELECT * FROM commits"
    return form_response(query)


@db_blueprint.route('/commits', methods=['GET'])
def get_daily_commits():
    query = "SELECT * FROM daily_commits"
    return form_response(query)


@db_blueprint.route('/developers', methods=['GET'])
def get_daily_devs():
    query = "SELECT * FROM daily_devs"
    return form_response(query)


@db_blueprint.route('/summary_table', methods=['GET'])
def get_summary_table():
    query = "SELECT * FROM summary_table"
    return form_response(query)


@db_blueprint.route('/git_rate_limit', methods=['GET'])
def get_git_rate_limit():
    query = "SELECT * FROM git_rate_limit"
    return form_response(query)
