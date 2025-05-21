import pytest
from app import create_app, db
from app.models import Todo
from config import TestingConfig

@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application."""
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def init_database(app):
    """Fixture to initialize the database for each test function."""
    with app.app_context():
        db.create_all()
        yield db  # provide the database instance
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def new_todo(init_database):
    """Fixture to create a new Todo item for testing."""
    todo = Todo(title="Test Todo", description="Test Description")
    init_database.session.add(todo)
    init_database.session.commit()
    return todo
