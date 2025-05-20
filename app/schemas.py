from marshmallow import Schema, fields, validate, ValidationError, post_load
from .models import Todo

class TodoSchema(Schema):
    id = fields.Int(dump_only=True)  # read-only field (only included in serialized output)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    description = fields.Str(required=False, allow_none=True, validate=validate.Length(max=500))
    completed = fields.Bool(required=False, default=False)
    created_at = fields.DateTime(dump_only=True)  # read-only
    updated_at = fields.DateTime(dump_only=True)  # read-only
    
    def validate_title(self, title):
        if title.strip() == "":
            raise ValidationError("Title cannot be empty or just whitespace.")
        
    @post_load
    def make_todo(self, data, **kwargs):
        return Todo(**data)
    
# Create schema instances for different use cases
todo_schema = TodoSchema()           # for single Todo serialization/deserialization
todos_schema = TodoSchema(many=True) # for multiple Todos