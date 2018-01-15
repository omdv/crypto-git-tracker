from flask import Blueprint
from project import create_app

celery_routes_2 = Blueprint('celery_2', __name__, template_folder='templates')
app, cel = create_app()


@cel.task(name='return_something_2')
def return_something_2():
    print('something_2')
    return 'something_2'


@celery_routes_2.route('/celery_2')
def celery_2():
    result = return_something_2.delay()
    return result.wait()