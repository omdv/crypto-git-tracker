import unittest
import coverage
import datetime as dt
from flask_script import Manager
from project import create_app, db
from project.api.models import Commit
from project.tests.custom_test_runner import TimeLoggingTestResult

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()


app, cel = create_app()
manager = Manager(app)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(resultclass=TimeLoggingTestResult).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(Commit(author='michael', message="Test #1", type="doc", date=dt.datetime.today()))
    db.session.add(Commit(author='bob', message="Test #2", type="algo", date=dt.datetime.today()))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
