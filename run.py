from app import create_app
import os

# Get the environment from FLASK_ENV or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))