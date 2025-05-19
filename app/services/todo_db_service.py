from app import db
from app.models import Todo

class TodoService:
    
    @staticmethod
    def get_all_todos():
        return Todo.query.all()
    
    @staticmethod
    def get_todo_by_id(todo_id):
        return Todo.query.get(todo_id)
    
    @staticmethod
    def create_todo(data):
        new_todo = Todo(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        
        db.session.add(new_todo)
        db.session.commit()
        return new_todo
    
    @staticmethod
    def update_todo(todo, data):
        if 'title' in data:
            todo.title = data['title']
        if 'description' in data:
            todo.description = data['description']
        if 'completed' in data:
            todo.completed = data['completed']
            
        db.session.commit()
        return todo
    
    @staticmethod
    def delete_todo(todo):
        db.session.delete(todo)
        db.session.commit()
        return True