from flask_script import Manager
from project import create_app

app, celery = create_app()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
