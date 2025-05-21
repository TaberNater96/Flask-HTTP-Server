import pytest
from app.models import Todo
from datetime import datetime

def test_new_todo_defaults(init_database):
    todo = Todo(title="Default Test")
    init_database.session.add(todo)
    init_database.session.commit()
    assert todo.id is not None
    assert todo.title == "Default Test"
    assert todo.description is None
    assert todo.completed is False
    assert isinstance(todo.created_at, datetime)

def test_new_todo_with_all_fields(init_database):
    timestamp = datetime.utcnow()
    todo = Todo(
        title="Full Todo", 
        description="Detailed description here", 
        completed=True,
        created_at=timestamp
    )
    init_database.session.add(todo)
    init_database.session.commit()
    assert todo.title == "Full Todo"
    assert todo.description == "Detailed description here"
    assert todo.completed is True
    assert todo.created_at == timestamp

def test_todo_to_dict(init_database):
    todo = Todo(title="Dict Test", description="Testing to_dict")
    init_database.session.add(todo)
    init_database.session.commit()
    
    todo_dict = todo.to_dict()
    
    assert todo_dict['id'] == todo.id
    assert todo_dict['title'] == "Dict Test"
    assert todo_dict['description'] == "Testing to_dict"
    assert todo_dict['completed'] is False
    assert 'created_at' in todo_dict
    # Ensure created_at is in ISO format string as per the model's to_dict
    assert isinstance(todo_dict['created_at'], str)
    try:
        datetime.fromisoformat(todo_dict['created_at'].replace('Z', '+00:00'))
    except ValueError:
        pytest.fail("created_at is not a valid ISO format string")

def test_todo_repr(init_database):
    todo = Todo(title="Repr Test")
    init_database.session.add(todo)
    init_database.session.commit()
    expected_repr = f"<Todo {todo.id}: Repr Test>"
    assert repr(todo) == expected_repr