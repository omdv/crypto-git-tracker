import os
from flask import Flask
from flask_cors import CORS
from celery import Celery
from datetime import timedelta


# Flask app factory
def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # register blueprints
    from project.api.routes import celery_routes
    app.register_blueprint(celery_routes)

    from project.api.routes_2 import celery_routes_2
    app.register_blueprint(celery_routes_2)

    app.config['CELERY_BACKEND_URL'] = "redis://redis:6379/0"
    app.config['CELERY_BROKER_URL'] = "redis://redis:6379/0"

    app.config['CELERYBEAT_SCHEDULE'] = {
        'say-every-5-seconds': {
            'task': 'return_something',
            'schedule': timedelta(seconds=5)
        },
        'say-every-10-seconds': {
            'task': 'return_something_2',
            'schedule': timedelta(seconds=10)
        },
    }
    app.config['CELERY_TIMEZONE'] = 'UTC'

    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
                celery.Task = ContextTask

    return app, celery
