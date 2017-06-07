
import os
import unittest
import coverage
COV = coverage.coverage(
    branch=True,
    omit=[
        '*/*bc/*',
        'manage.py/*',
        'app/errors.py'
        'tests/base.py',
        'tests/test_authentication.py',
        'tests/test_endpoints.py'
        'instance/config.py',
        '/*/__init__.py'
    ]
)
COV.start()

from flask_script import Manager, prompt_bool, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app.models import User, Bucketlist, Item

# create the app
app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)


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

# manually create_db
@manager.command
def create_db():
    """Creates database tables from models"""
    db.create_all()
    print ('Intialized....!')

# manually drop db
@manager.command
def drop_db():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
        print ('Db droped....!')


def make_shell_context():
    return dict(User=User,
                Bucketlist=Bucketlist,
                Item=Item)

# Allows us to make migrations using the db command
# Allows use to access shell as above.


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
