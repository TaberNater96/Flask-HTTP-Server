from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError
from app.models import db, Todo
from ..schemas import todo_schema, todos_schema

api_bp = Blueprint('api', __name__)

@api_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    result = todos_schema.dump(todos)
    return jsonify(result), 200

@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    result = todo_schema.dump(todo)
    return jsonify(result), 200

@api_bp.route('/todos', methods=['POST'])
def create_todo():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
        
    try:
        # Validate and deserialize input
        todo_data = todo_schema.load(json_data)
        
        # Create new Todo object
        new_todo = Todo(
            title=todo_data['title'],
            description=todo_data.get('description', ''),
            completed=todo_data.get('completed', False)
        )
        
        # Save to database
        db.session.add(new_todo)
        db.session.commit()
        
        # Return the created todo
        result = todo_schema.dump(new_todo)
        return jsonify(result), 201
        
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    json_data = request.get_json()
    
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        # Partial load allows updating only some fields
        todo_data = todo_schema.load(json_data, partial=True)
        
        # Update fields if they exist in the request
        if 'title' in todo_data:
            todo.title = todo_data['title']
        if 'description' in todo_data:
            todo.description = todo_data['description']
        if 'completed' in todo_data:
            todo.completed = todo_data['completed']
        
        db.session.commit()
        
        result = todo_schema.dump(todo)
        return jsonify(result), 200
        
    except ValidationError as err:
        return jsonify({"message": "Validation error", "errors": err.messages}), 400

@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted'}), 200