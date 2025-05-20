from app import create_app
import os

# Get the environment from FLASK_ENV or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # The host='0.0.0.0' makes the server accessible externally, not just on localhost.
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) # debug=True will be set based on the FLASK_ENV via the config.