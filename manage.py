
import os
import unittest
import coverage
COV = coverage.coverage(
    branch=True,
    omit=[
        '*/*bc/*',
        'bucketlist/*',
        'tests/*',
        'config.py',
        '/*/__init__.py'
    ]
)
COV.start()

from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Bucketlist, Item

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=1).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    """Creates database tables from models"""
    db.create_all()
    print ('Intialized....!')


@manager.command
def drop_db():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print ('Db droped....!')


if __name__ == '__main__':
    manager.run()
