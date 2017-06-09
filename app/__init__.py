from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from config import config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from app.authentication import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.endpoints import bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)
    # pass flask object to db object
    db.init_app(app)

    return app
