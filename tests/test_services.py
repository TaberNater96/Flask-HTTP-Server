import pytest
from app.services.todo_db_service import TodoService
from app.models import Todo
from app import db

# --- Test get_all_todos --- #
def test_get_all_todos_empty_db(init_database):
    todos = TodoService.get_all_todos()
    assert todos == []

def test_get_all_todos_with_items(init_database):
    todo1 = Todo(title="Service Test 1", description="Desc 1")
    todo2 = Todo(title="Service Test 2", description="Desc 2", completed=True)
    db.session.add_all([todo1, todo2])
    db.session.commit()

    todos = TodoService.get_all_todos()
    assert len(todos) == 2
    assert todos[0].title == "Service Test 1"
    assert todos[1].title == "Service Test 2"
    assert todos[1].completed is True

# --- Test get_todo_by_id --- #
def test_get_todo_by_id_exists(init_database):
    todo = Todo(title="Find Me", description="I am here")
    db.session.add(todo)
    db.session.commit()

    found_todo = TodoService.get_todo_by_id(todo.id)
    assert found_todo is not None
    assert found_todo.id == todo.id
    assert found_todo.title == "Find Me"

def test_get_todo_by_id_not_exists(init_database):
    found_todo = TodoService.get_todo_by_id(999) # Assuming 999 does not exist
    assert found_todo is None

# --- Test create_todo --- #
def test_create_todo_service(init_database):
    # The service method expects a Todo ORM instance (created by schema.load)
    new_todo_obj = Todo(title="Service Create", description="Created via service")
    
    created_todo = TodoService.create_todo(new_todo_obj)
    assert created_todo is not None
    assert created_todo.id is not None # Should have an ID after commit
    assert created_todo.title == "Service Create"
    assert created_todo.description == "Created via service"
    assert created_todo.completed is False # Default

    # Verify it's in the database
    db_todo = Todo.query.get(created_todo.id)
    assert db_todo is not None
    assert db_todo.title == "Service Create"

# --- Test update_todo --- #
def test_update_todo_service_full_update(init_database):
    original_todo = Todo(title="Original Title", description="Original Desc")
    db.session.add(original_todo)
    db.session.commit()
    update_data_dict = {"title": "Updated Title", "description": "Updated Desc", "completed": True}
    validated_obj_for_service = Todo(title="Updated Title", description="Updated Desc", completed=True)
    updated_todo = TodoService.update_todo(original_todo, update_data_dict, validated_obj_for_service)
    assert updated_todo is not None
    assert updated_todo.id == original_todo.id
    assert updated_todo.title == "Updated Title"
    assert updated_todo.description == "Updated Desc"
    assert updated_todo.completed is True
    db_todo = Todo.query.get(original_todo.id)
    assert db_todo.title == "Updated Title"
    assert db_todo.completed is True

def test_update_todo_service_partial_update(init_database):
    original_todo = Todo(title="Partial Original", description="Partial Desc")
    db.session.add(original_todo)
    db.session.commit()
    update_data_dict = {"completed": True} # this is the raw json_data
    validated_obj_for_service = Todo(title=None, description=None, completed=True) # title/desc would be None if not in partial_data
    updated_todo = TodoService.update_todo(original_todo, update_data_dict, validated_obj_for_service)
    assert updated_todo.title == "Partial Original" # should not change
    assert updated_todo.description == "Partial Desc" # should not change
    assert updated_todo.completed is True
    db_todo = Todo.query.get(original_todo.id)
    assert db_todo.completed is True
    assert db_todo.title == "Partial Original"

def test_update_todo_service_non_existent(init_database):
    non_existent_todo_instance = Todo(id=999, title="Ghost")
    update_data = {"title": "New Ghost Title"}
    validated_obj = Todo(title="New Ghost Title")
    with pytest.raises(Exception): # or a more specific SQLAlchemy error if it tries to operate on a detached instance
        TodoService.update_todo(non_existent_todo_instance, update_data, validated_obj)
    
    assert Todo.query.get(999) is None # ensure it didn't magically create it


# --- Test delete_todo --- #
def test_delete_todo_service_existing(init_database):
    todo_to_delete = Todo(title="To Be Deleted")
    db.session.add(todo_to_delete)
    db.session.commit()
    todo_id = todo_to_delete.id

    TodoService.delete_todo(todo_to_delete)
    
    assert Todo.query.get(todo_id) is None

def test_delete_todo_service_non_existent_instance(init_database):
    # Similar to update, the service expects a valid ORM instance that's in the session.
    non_persistent_todo = Todo(title="Never Existed")
    # Calling delete on a non-persistent object might not error immediately but won't affect the database.
    try:
        TodoService.delete_todo(non_persistent_todo)
        # If it doesn't error, we just check that nothing was actually deleted from DB if it had an ID
        if non_persistent_todo.id:
             assert Todo.query.get(non_persistent_todo.id) is None
    except Exception as e:
        pass # error is acceptable if it's due to detached instance