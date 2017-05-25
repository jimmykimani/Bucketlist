import os

class Config(object):
    """
    common configuration settings
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

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
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/test_db'
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

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
