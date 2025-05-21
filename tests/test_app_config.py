from flask import Flask
from config import Config, DevelopmentConfig, TestingConfig, ProductionConfig

def test_default_config(app):
    app = Flask(__name__)
    app.config.from_object(Config())
    app.config.from_object(DevelopmentConfig())
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False
    assert 'SQLALCHEMY_DATABASE_URI' in app.config

def test_development_config(app):
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig())
    assert app.config['DEBUG'] is True
    assert 'SQLALCHEMY_DATABASE_URI' in app.config

def test_testing_config(app):
    app = Flask(__name__)
    app.config.from_object(TestingConfig())
    assert app.config['TESTING'] is True
    assert app.config['DEBUG'] is True
    assert 'SQLALCHEMY_DATABASE_URI' in app.config
    assert 'sqlite:///:memory:' in app.config['SQLALCHEMY_DATABASE_URI']

def test_production_config(app):
    app = Flask(__name__)
    app.config.from_object(ProductionConfig())
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False
    assert 'SQLALCHEMY_DATABASE_URI' in app.config

from app import create_app

def test_create_app_development():
    app = create_app(DevelopmentConfig)
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False

def test_create_app_testing():
    app = create_app(TestingConfig)
    assert app.config['TESTING'] is True
    assert 'sqlite:///:memory:' in app.config['SQLALCHEMY_DATABASE_URI']

def test_create_app_production():
    app = create_app(ProductionConfig)
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False