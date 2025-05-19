from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name:
        from config import config
        cfg = config.get(config_name, 'default')
        app.config.from_object(cfg)
        
        if hasattr(cfg, 'init_app'):
            cfg.init_app(app)
    else:
        # Default configuration based on environment
        from config import config
        env = os.environ.get('FLASK_ENV', 'development')
        app.config.from_object(config[env])
        
        # Call init_app if it exists
        if hasattr(config[env], 'init_app'):
            config[env].init_app(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return render_template('index.html') 
    
    return app