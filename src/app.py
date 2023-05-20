from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from todo import TodoService

todo_service = TodoService()

logger = Logger(service="Todos.app")
app = APIGatewayRestResolver()


# List all todos in table
@app.get("/todos")
def list_todos():
    return todo_service.list()


# Create a new todo
@app.post("/todos")
def create_todo():
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    return todo_service.create(todo_data=todo_data)


# Retrieve a particular todo by by id
@app.get("/todos/<id>")
def get_todo_by_id(id):
    return todo_service.get(id=id)


# Update a particular to todo by id
@app.put("/todos/<id>")
def update_todo(id):
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    return todo_service.update(todo_data={**todo_data, "id": id})


# Delete a particular to todo by id
@app.delete("/todos/<id>")
def delete_todo(id):
    return todo_service.delete(id=id)


def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
