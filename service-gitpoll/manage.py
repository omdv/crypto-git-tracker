# manage.py


import time
import unittest
from flask_script import Manager
from project import app


manager = Manager(app)
polling = False


@manager.option('-d', '--delay', help='Delay in seconds', dest="poll_delay")
def start_poll(poll_delay):
    polling = True
    while polling:
        print("polling")
        time.sleep(int(poll_delay))


@manager.command
def stop_poll():
    polling = False


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
