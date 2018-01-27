# project/api/views.py
import pandas as pd

from flask import Blueprint, Response
from flask import current_app as app

from sqlalchemy import create_engine

# globals
db_blueprint = Blueprint('db', __name__)


# @db_blueprint.route('/commits', methods=['GET'])
# def get_all_commits():
#     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#     df = pd.read_sql('commits', engine)
#     response_object = {
#         'status': 'success',
#         'data': {
#             'commits': df.to_dict(orient='records')
#         }
#     }
#     return jsonify(response_object), 200


# @db_blueprint.route('/initial_download', methods=['POST'])
# def post_initial_download():
#     post_data = request.get_json()

#     # update configuration of watcher
#     watcher.set_app_config(app.config)

#     # TEST case
#     if post_data:
#         if post_data.get('test'):
#             watcher.set_page_limit(post_data.get('page_limit'))
#             executor.submit(watcher.initial_download)
#     # NON TEST CASE
#     else:
#         watcher.set_page_limit(1e6)
#         executor.submit(watcher.initial_download)

#     response_object = {
#         'status': 'success',
#         'message': f'Initial download...'
#     }
#     return jsonify(response_object), 201


# @db_blueprint.route('/start_poll', methods=['POST'])
# def post_start_poll():
#     post_data = request.get_json()

#     # update configuration of watcher
#     watcher.set_app_config(app.config)

#     # TEST case
#     if post_data:
#         if post_data.get('test'):
#             watcher.set_page_limit(post_data.get('page_limit'))
#             executor.submit(watcher.initial_download)

#     # TODO: BUSINESS LOGIC HERE
#     # watcher.set_page_limit(3)

#     response_object = {
#         'status': 'success',
#         'message': f'Polling has started!'
#     }
#     return jsonify(response_object), 201


# @db_blueprint.route('/stop_poll', methods=['POST'])
# def post_stop_poll():
#     # update configuration of watcher
#     watcher.set_app_config(app.config)

#     # stop polling
#     watcher.set_polling(False)

#     response_object = {
#         'status': 'success',
#         'message': f'Polling was stopped!'
#     }
#     return jsonify(response_object), 201


# @db_blueprint.route('/git_rate_limit', methods=['GET'])
# def get_git_rate_limit():

#     # update configuration of watcher
#     watcher.set_app_config(app.config)

#     response_object = {
#         'status': 'success',
#         'data': {
#             'rate_limit': watcher.get_rate_limit()
#         }
#     }
#     return jsonify(response_object), 200


@db_blueprint.route('/daily_commits', methods=['GET'])
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


# @db_blueprint.route('/summary_table', methods=['GET'])
# def get_summary_table():
#     # analytics = GitAnalytics(app.config)
#     # _ = analytics.summary_table()

#     engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
#     df = pd.read_sql('summary_table', engine)

#     resp = Response(
#         response=df.to_json(orient='records'),
#         status=200,
#         mimetype="application/json")

#     resp.headers['Access-Control-Allow-Origin'] = '*'
#     return resp


@db_blueprint.route('/test', methods=['GET'])
def test_db():
    return "test passed", 200
