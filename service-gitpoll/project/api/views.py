# project/api/views.py


from flask import Blueprint, jsonify, request

from project.api.models import Commit
from project import db


analytics_blueprint = Blueprint('analytics', __name__)


@analytics_blueprint.route('/start_poll', methods=['POST'])
def post_start_poll():
    """Starting poll with given delay"""
    post_data = request.get_json()
    delay = post_data.get('delay')

    # TODO: BUSINESS LOGIC HERE

    response_object = {
        'status': 'success',
        'message': f'Polling has started ({delay}sec)!'
    }
    return jsonify(response_object), 201
