import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    common configuration settings
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'bucketlist.sqlite')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    Configuration settings for development
    """
    DEBUG = True



class TestingConfig(Config):
    """
    Configurations for Testing
    """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir,
                                                           'bucketlist.db'))
    DEBUG = True


class StagingConfig(Config):
    """
    Configurations for Staging.
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Configurations for Production.
    """
    DEBUG = False
    TESTING = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
