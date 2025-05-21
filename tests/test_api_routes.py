import json
from app.models import Todo
from app import db

# --- Test GET /api/todos ---
def test_get_all_todos_empty(client, init_database):
    response = client.get('/api/todos')
    assert response.status_code == 200
    assert response.json == []

def test_get_all_todos_with_data(client, init_database):
    todo1 = Todo(title="Todo 1", description="First todo")
    todo2 = Todo(title="Todo 2", description="Second todo", completed=True)
    db.session.add_all([todo1, todo2])
    db.session.commit()

    response = client.get('/api/todos')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 2
    assert data[0]["title"] == "Todo 1"
    assert data[1]["title"] == "Todo 2"
    assert data[1]["completed"] is True

# --- Test GET /api/todos/<id> ---
def test_get_specific_todo_exists(client, new_todo):
    response = client.get(f'/api/todos/{new_todo.id}')
    assert response.status_code == 200
    data = response.json
    assert data["id"] == new_todo.id
    assert data["title"] == new_todo.title
    assert data["description"] == new_todo.description

def test_get_specific_todo_not_exists(client, init_database):
    response = client.get('/api/todos/999')
    assert response.status_code == 404
    assert "not found" in response.json["description"].lower()

# --- Test POST /api/todos ---
def test_create_todo_success(client, init_database):
    payload = {"title": "New Shiny Todo", "description": "This is important!"}
    response = client.post('/api/todos', json=payload)
    assert response.status_code == 201
    data = response.json
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["completed"] is False # Default
    assert "id" in data
    # Verify it was actually saved to DB
    todo = Todo.query.get(data["id"])
    assert todo is not None
    assert todo.title == payload["title"]

def test_create_todo_no_data(client, init_database):
    response = client.post('/api/todos', data=json.dumps({}), content_type='application/json')
    response_no_data = client.post('/api/todos')
    assert response_no_data.status_code == 400
    assert "No input data provided" in response_no_data.json["description"]

def test_create_todo_missing_title(client, init_database):
    payload = {"description": "A todo without a title"}
    response = client.post('/api/todos', json=payload)
    assert response.status_code == 400
    assert "title" in response.json
    assert "Missing data for required field." in response.json["title"]

def test_create_todo_invalid_title_too_short(client, init_database):
    payload = {"title": "T", "description": "A todo"}
    response = client.post('/api/todos', json=payload)
    assert response.status_code == 400
    assert "title" in response.json
    assert "Title must be between 2 and 100 characters long." in response.json["title"][0]

# --- Test PUT /api/todos/<id> ---
def test_update_todo_success_full(client, new_todo):
    payload = {"title": "Updated Title", "description": "Updated Description", "completed": True}
    response = client.put(f'/api/todos/{new_todo.id}', json=payload)
    assert response.status_code == 200
    data = response.json
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["completed"] == payload["completed"]
    # Verify DB update
    updated_todo_from_db = Todo.query.get(new_todo.id)
    assert updated_todo_from_db.title == payload["title"]
    assert updated_todo_from_db.completed is True

def test_update_todo_success_partial(client, new_todo):
    payload = {"completed": True}
    response = client.put(f'/api/todos/{new_todo.id}', json=payload)
    assert response.status_code == 200
    data = response.json
    assert data["title"] == new_todo.title
    assert data["completed"] is True
    updated_todo_from_db = Todo.query.get(new_todo.id)
    assert updated_todo_from_db.completed is True

def test_update_todo_not_found(client, init_database):
    payload = {"title": "Won't Update"}
    response = client.put('/api/todos/999', json=payload)
    assert response.status_code == 404
    assert "not found" in response.json["description"].lower()

def test_update_todo_no_data(client, new_todo):
    response = client.put(f'/api/todos/{new_todo.id}')
    assert response.status_code == 400
    assert "No input data provided" in response.json["description"]

def test_update_todo_invalid_data(client, new_todo):
    payload = {"title": "T"}
    response = client.put(f'/api/todos/{new_todo.id}', json=payload)
    assert response.status_code == 400
    assert "title" in response.json
    assert "Title must be between 2 and 100 characters long." in response.json["title"][0]

# --- Test DELETE /api/todos/<id> ---
def test_delete_todo_success(client, new_todo):
    response = client.delete(f'/api/todos/{new_todo.id}')
    assert response.status_code == 200
    assert "deleted successfully" in response.json["message"]
    deleted_todo = Todo.query.get(new_todo.id)
    assert deleted_todo is None

def test_delete_todo_not_found(client, init_database):
    response = client.delete('/api/todos/999')
    assert response.status_code == 404
    assert "not found" in response.json["description"].lower()

# Test root route
def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data or b"<title>Todo App</title>" in response.data