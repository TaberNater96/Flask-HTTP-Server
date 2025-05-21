from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'development') # defined in .env

    from config import config
    cfg = config.get(config_name)
    if not cfg:
        app.logger.warning(f"Config '{config_name}' not found, defaulting to 'development'.")
        cfg = config['development'] # fallback to development if config_name is invalid
    
    app.config.from_object(cfg)
    app.logger.info(f"Application configured with {config_name.capitalize()}Config.")

    # Initialize extensions and app-specific configurations
    if hasattr(cfg, 'init_app'):
        cfg.init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register Blueprints
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.logger.info("API blueprint registered.")
    
    # Basic route for serving the frontend
    @app.route('/')
    def index():
        app.logger.info("Serving index.html")
        return render_template('index.html') 
    
    app.logger.info("Flask app creation complete.")
    return app