from flask import Blueprint
from project import create_app

celery_routes = Blueprint('celery', __name__, template_folder='templates')
app, cel = create_app()


@cel.task(name='return_something')
def return_something():
    print('something')
    return 'something'


@celery_routes.route('/celery')
def celery():
    result = return_something.delay()
    return result.wait()


@celery_routes.route('/test')
def test():
    return "test", 200