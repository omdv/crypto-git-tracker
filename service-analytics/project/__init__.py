import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from celery import Celery

# instantiate the db
db = SQLAlchemy()


# Flask app factory
def create_app():
    # instantiate the app
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.db_endpoints import db_blueprint
    app.register_blueprint(db_blueprint)

    # register celery app
    celery = Celery(
        app.import_name,
        include=[
            'project.tasks.summary',
            'project.tasks.watcher',
            'project.tasks.rate_limit'],
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    # define celery task with app_context
    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
                celery.Task = ContextTask

    return app, celery
