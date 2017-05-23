import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates database tables from sqlalchemy models"""
    app = create_app('default')
    with app.app_context():
        db.create_all()


@manager.command
def drop_db():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data?"):
        app = create_app('default')
        with app.app_context():
            db.drop_all()


if __name__ == '__main__':
    manager.run()
