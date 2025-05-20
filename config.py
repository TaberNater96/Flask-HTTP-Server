import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False # set to True for verbose SQL query logging, False for cleaner app logs
    
    # Logging
    LOG_LEVEL = logging.INFO # default log level
    LOG_FILE = os.path.join(basedir, 'logs/app.log')
    LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    
    @classmethod
    def init_app(cls, app):
        if not os.path.exists(os.path.join(basedir, 'logs')):
            os.makedirs(os.path.join(basedir, 'logs'))

        file_handler = RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=10240,  # 10KB per file
            backupCount=10   # keep 10 backup files
        )
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(cls.LOG_LEVEL)
        app.logger.addHandler(file_handler)

        # Console Handler (for development and general visibility)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        console_handler.setLevel(cls.LOG_LEVEL) # or a different level for console if needed
        app.logger.addHandler(console_handler)
        
        app.logger.setLevel(cls.LOG_LEVEL)
        app.logger.info('Flask Todo API logging initialized.')


class DevelopmentConfig(Config):
    DEBUG = True
    # Use the set environment database URL, if it is not found in the environment settings, then use default postgres path
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/http_todo')
    SQLALCHEMY_ECHO = False # keep this False to avoid duplicate SQL logs since app.logger is used 
    LOG_LEVEL = logging.DEBUG # more verbose logging for development

    @classmethod
    def init_app(cls, app):
        Config.init_app(app) # call base class init_app
        app.logger.info('Development configuration loaded.')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/http_todo')
    LOG_LEVEL = logging.DEBUG

    @classmethod
    def init_app(cls, app):
        Config.init_app(app) # call base class init_app
        app.logger.info('Testing configuration loaded.')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/http_todo')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LOG_LEVEL = logging.INFO # standard logging for production
    
    # Make sure the SECRET_KEY is set for production
    @classmethod
    def init_app(cls, app):
        Config.init_app(app) # call base class init_app
        app.logger.info('Production configuration loaded.')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}