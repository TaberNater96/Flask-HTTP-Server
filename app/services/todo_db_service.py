from app import db
from app.models import Todo
from flask import current_app

class TodoService:
    """
    Service class for handling business logic related to Todo items.
    This class encapsulates all database interactions for Todo objects.
    """
    
    @staticmethod
    def get_all_todos():
        """
        Retrieves all Todo items from the database.

        Returns:
            list: A list of all Todo objects.
        """
        current_app.logger.debug("TodoService: Retrieving all todos from DB.")
        return Todo.query.all()
    
    @staticmethod
    def get_todo_by_id(todo_id):
        """
        Retrieves a specific Todo item by its ID.

        Args:
            todo_id (int): The ID of the Todo item to retrieve.

        Returns:
            Todo: The Todo object if found, otherwise None.
        """
        current_app.logger.debug(f"TodoService: Retrieving todo with ID {todo_id} from DB.")
        return Todo.query.get(todo_id)
    
    @staticmethod
    def create_todo(new_todo_obj):
        """
        Creates a new Todo item in the database.
        
        Note that new_todo_obj is the Todo instance from schema.load()

        Args:
            new_todo_obj (Todo): The Todo object to be added to the database.
                                 This object is typically created from validated schema data.

        Returns:
            Todo: The newly created Todo object, now persisted with an ID.
        """
        current_app.logger.debug(f"TodoService: Creating new todo: {new_todo_obj.title[:20]}...") # log snippet of title
        db.session.add(new_todo_obj) 
        db.session.commit() 
        current_app.logger.info(f"TodoService: Successfully created todo with ID {new_todo_obj.id}.")
        return new_todo_obj
    
    @staticmethod
    def update_todo(todo_orm_instance, request_json_data, validated_partial_obj):
        """
        Updates an existing Todo item in the database.

        This method selectively updates fields of a Todo item based on the
        provided JSON data and a validated partial Todo object.

        Args:
            todo_orm_instance (Todo): The ORM instance of the Todo item to be updated.
            request_json_data (dict): The raw JSON data received in the request.
                                      Used to check which fields were actually sent for update.
            validated_partial_obj (Todo): A Todo object (potentially partially populated)
                                          containing validated data for the fields to be updated.

        Returns:
            Todo: The updated Todo ORM instance.
        """
        current_app.logger.debug(f"TodoService: Updating todo with ID {todo_orm_instance.id}.")
        updated_fields = []
        if 'title' in request_json_data:
            todo_orm_instance.title = validated_partial_obj.title
            updated_fields.append('title')
        if 'description' in request_json_data:
            todo_orm_instance.description = validated_partial_obj.description
            updated_fields.append('description')
        if 'completed' in request_json_data:
            todo_orm_instance.completed = validated_partial_obj.completed
            updated_fields.append('completed')
            
        db.session.commit()
        current_app.logger.info(f"TodoService: Successfully updated fields {updated_fields} for todo ID {todo_orm_instance.id}.")
        return todo_orm_instance
    
    @staticmethod
    def delete_todo(todo):
        """
        Deletes a Todo item from the database.

        Args:
            todo (Todo): The Todo ORM instance to be deleted.

        Returns:
            bool: True if the deletion was successful.
        """
        todo_id = todo.id # capture id before deletion
        current_app.logger.debug(f"TodoService: Deleting todo with ID {todo_id}.")
        db.session.delete(todo)
        db.session.commit()
        current_app.logger.info(f"TodoService: Successfully deleted todo with ID {todo_id}.")
        return True  # confirms successful deletion.