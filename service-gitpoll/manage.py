# manage.py

import unittest
from flask_script import Manager
from project import app, start_git_poll, stop_git_poll


manager = Manager(app)


@manager.option('-d', '--delay', help='Delay in seconds', dest="poll_delay")
def start_poll(poll_delay):
    start_git_poll(poll_delay)


@manager.command
def stop_poll():
    stop_git_poll()


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
