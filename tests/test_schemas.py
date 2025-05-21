import pytest
from marshmallow import ValidationError
from app.schemas import TodoSchema
from app.models import Todo
from datetime import datetime

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

# Test data
valid_todo_data = {
    "title": "Test Todo",
    "description": "A description for the test todo"
}

valid_todo_data_full = {
    "title": "Test Todo Full",
    "description": "A full description",
    "completed": True
}

# --- Serialization Tests (dump) ---

def test_serialize_todo_model_instance(new_todo):
    result = todo_schema.dump(new_todo)
    assert result["id"] == new_todo.id
    assert result["title"] == new_todo.title
    assert result["description"] == new_todo.description
    assert result["completed"] == new_todo.completed
    assert "created_at" in result
    # Make sure created_at is serialized to ISO format string
    assert isinstance(result["created_at"], str)
    datetime.fromisoformat(result["created_at"].replace('Z', '+00:00')) # validate format

def test_serialize_multiple_todo_model_instances(init_database):
    todo1 = Todo(title="Todo 1", description="First todo")
    todo2 = Todo(title="Todo 2", description="Second todo", completed=True)
    init_database.session.add_all([todo1, todo2])
    init_database.session.commit()

    todos = [todo1, todo2]
    result = todos_schema.dump(todos)
    assert len(result) == 2
    assert result[0]["title"] == "Todo 1"
    assert result[1]["title"] == "Todo 2"
    assert result[1]["completed"] is True

# --- Deserialization Tests (load) ---

def test_deserialize_valid_data_to_todo_object():
    # The schema's load method by default returns a dictionary if not configured with make_instance
    todo_obj = todo_schema.load(valid_todo_data)
    assert isinstance(todo_obj, Todo) # check if make_todo returned a Todo ORM instance
    assert todo_obj.title == valid_todo_data["title"]
    assert todo_obj.description == valid_todo_data["description"]
    assert todo_obj.completed is False # default value from model

def test_deserialize_valid_data_full_to_todo_object():
    todo_obj = todo_schema.load(valid_todo_data_full)
    assert isinstance(todo_obj, Todo)
    assert todo_obj.title == valid_todo_data_full["title"]
    assert todo_obj.description == valid_todo_data_full["description"]
    assert todo_obj.completed == valid_todo_data_full["completed"]

# --- Validation Tests --- 

def test_validate_missing_title():
    invalid_data = {"description": "A todo without a title"}
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(invalid_data)
    assert "title" in excinfo.value.messages
    assert "Missing data for required field." in excinfo.value.messages["title"]

def test_validate_title_too_short():
    invalid_data = {"title": "T", "description": "Short title"}
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(invalid_data)
    assert "title" in excinfo.value.messages
    assert "Title must be between 2 and 100 characters long." in excinfo.value.messages["title"][0]

def test_validate_title_too_long():
    invalid_data = {"title": "T" * 101, "description": "Long title"}
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(invalid_data)
    assert "title" in excinfo.value.messages
    assert "Title must be between 2 and 100 characters long." in excinfo.value.messages["title"][0]

def test_validate_title_whitespace_only():
    invalid_data = {"title": "   ", "description": "Whitespace title"}
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(invalid_data)
    assert "title" in excinfo.value.messages
    assert "Title cannot be empty or just whitespace." in excinfo.value.messages["title"][0]

def test_validate_description_too_long():
    invalid_data = {"title": "Valid Title", "description": "D" * 201}
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(invalid_data)
    assert "description" in excinfo.value.messages
    assert "Description cannot exceed 200 characters." in excinfo.value.messages["description"][0]

def test_deserialize_unknown_field():
    data_with_unknown = {"title": "Test Unknown", "extra_field": "should be ignored"}
    try:
        todo_obj = todo_schema.load(data_with_unknown)
        assert todo_obj.title == "Test Unknown"
        assert not hasattr(todo_obj, "extra_field")
    except ValidationError:
        pytest.fail("Deserialization failed with unknown field, check schema EXCLUDE behavior.")

def test_make_todo_method():
    data = {"title": "Make Me", "description": "A todo from make_todo"}
    todo_instance = todo_schema.make_todo(data)
    assert isinstance(todo_instance, Todo)
    assert todo_instance.title == data["title"]
    assert todo_instance.description == data["description"]
    assert todo_instance.completed is False # Default

# Test partial updates (deserialization)
def test_deserialize_partial_data():
    partial_data = {"description": "Updated Description Only"}
    # When loading partial, it should not raise validation error for missing 'title'
    try:
        update_data_dict = todo_schema.load(partial_data, partial=True)
        assert "title" not in update_data_dict # title was not provided, so not in result
        assert update_data_dict["description"] == "Updated Description Only"
    except ValidationError as e:
        pytest.fail(f"Partial deserialization failed: {e.messages}")

def test_deserialize_partial_with_validation_error():
    partial_invalid_data = {"title": "T"} # title too short
    with pytest.raises(ValidationError) as excinfo:
        todo_schema.load(partial_invalid_data, partial=True)
    assert "title" in excinfo.value.messages
    assert "Title must be between 2 and 100 characters long." in excinfo.value.messages["title"][0]
