from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from ..schemas import todo_schema, todos_schema # schemas for serialization/deserialization
from ..services.todo_db_service import TodoService

api_bp = Blueprint('api', __name__)

@api_bp.route('/todos', methods=['GET'])
def get_todos():
    """Retrieve a list of all Todo items.

    This endpoint fetches all records from the Todo table in the database, serializes them using the todos_schema (which handles multiple items),
    and returns them as a JSON array.

    Returns:
        tuple: A Flask Response object containing the JSON list of todos and an HTTP status code 200 (OK).
    """
    todos = TodoService.get_all_todos() # fetch all Todo records from the database
    result = todos_schema.dump(todos)   # serialize the list of Todo objects into a JSON-compatible format
    return jsonify(result), 200

@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Retrieve a specific Todo item by its ID.

    This endpoint fetches a single Todo item from the database based on the provided todo_id. If the item is not found, it returns a 404 error.
    Otherwise, it serializes the item using todo_schema and returns it as JSON.

    Args:
        todo_id (int): The unique identifier of the Todo item to retrieve.

    Returns:
        tuple: A Flask Response object containing the JSON representation of the Todo item and an HTTP status code 200 (OK), or a 404 error response
               if the item is not found.
    """
    todo = TodoService.get_todo_by_id(todo_id)  # fetch the Todo item by ID; abort with 404 if not found
    if not todo:
        abort(404, description="Todo item not found")
        
    result = todo_schema.dump(todo)             # serialize the Todo object into a JSON-compatible format
    return jsonify(result), 200

@api_bp.route('/todos', methods=['POST'])
def create_todo():
    """Create a new Todo item.

    This endpoint accepts JSON data representing a new Todo item. It validates the input data using todo_schema. If validation is successful, a new Todo 
    record is created and saved to the database. The newly created item is then serialized and returned as JSON with an HTTP 201 status code. If input 
    data is missing or validation fails, appropriate error responses are returned.

    Returns:
        tuple: A Flask Response object containing the JSON representation of the newly created Todo item and an HTTP status code 201 (Created), or an 
        error response with status code 400 (Bad Request) if input is invalid or missing.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
        
    try:
        # Validate and deserialize the input JSON data against the todo_schema
        todo_data = todo_schema.load(json_data)
        new_todo = TodoService.create_todo(todo_data)
        
        # Serialize the newly created Todo object for the response back to client
        result = todo_schema.dump(new_todo)
        return jsonify(result), 201
        
    except ValidationError as err:
        # Handle Marshmallow validation errors
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update an existing Todo item by its ID.

    This endpoint allows for updating an existing Todo item identified by todo_id. It accepts JSON data containing the fields to be updated. The input 
    data is validated using todo_schema with partial loading enabled, allowing for updates to a subset of fields. If the item is found and data is valid,
    the item is updated in the database and the updated item is returned as JSON. Error responses are returned for missing items, missing input data, or
    validation failures.

    Args:
        todo_id (int): The unique identifier of the Todo item to update.

    Returns:
        tuple: A Flask Response object containing the JSON representation of the updated Todo item and an HTTP status code 200 (OK), or an error response 
        (404 if not found, 400 if input is invalid/missing).
    """
    todo = TodoService.get_todo_by_id(todo_id)  # fetch the Todo item by ID; abort with 404 if not found
    json_data = request.get_json()
    
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        # Validate and deserialize input, allowing partial updates (only fields present in json_data are processed)
        todo_data = todo_schema.load(json_data, partial=True)
        updated_todo = TodoService.update_todo(todo, todo_data)
        
        # Serialize the updated Todo object for the response back to client
        result = todo_schema.dump(updated_todo)
        return jsonify(result), 200
        
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a Todo item by its ID.

    This endpoint removes a Todo item from the database based on the provided todo_id. If the item is found, it is deleted, and a confirmation message
    is returned. If the item is not found, a 404 error is returned.

    Args:
        todo_id (int): The unique identifier of the Todo item to delete.

    Returns:
        tuple: A Flask Response object containing a success message and an HTTP status code 200 (OK), or a 404 error response if the item is not found.
    """
    todo = TodoService.get_todo_by_id(todo_id)  # fetch the Todo item by ID; abort with 404 if not found
    if not todo:
        abort(404, description="Todo item not found")
        
    TodoService.delete_todo(todo)
    return jsonify({'message': 'Todo deleted'}), 200