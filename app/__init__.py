from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from config import config

#intialize database sqlalchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # connect the app to the database
    db.init_app(app)

    return app
