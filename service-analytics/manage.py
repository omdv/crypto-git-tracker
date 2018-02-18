import unittest
import coverage
import datetime as dt
from flask_script import Manager
from project import create_app, db
from project.api.models import RepoControlRecord
from project.analytics.git_watcher import GitWatcher
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


def add_one_repo(repo):
    ticker, apihandle, url = repo.split(':')
    if_exists = len(db.session.query(
        RepoControlRecord.id).filter_by(url=url).all()) is not 0
    if not if_exists:
        db.session.add(RepoControlRecord(
            ticker=ticker, apihandle=apihandle, url=url))
        print("Repo {} was added".format(url))
        db.session.commit()
    else:
        print("Repo {} already exists".format(url))


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


@manager.option('-r', '--repo', help='ticker:apihandle:repo_url')
def add_repo_url(repo):
    add_one_repo(repo)


@manager.option('-f', '--filename', help='filename.csv')
def add_repos(filename):
    with open(filename, 'r') as _f:
        repos = _f.readlines()
    for _r in repos:
        add_one_repo(_r.strip('\n'))


@manager.command
def rate_limit():
    watcher = GitWatcher(None, None, None, dt.datetime(2000, 1, 1))
    watcher.set_app_config(app.config)
    print(watcher.get_rate_limit())


if __name__ == '__main__':
    manager.run()
