from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from todo import TodoService

todo_service = TodoService()

logger = Logger(service="Todos")
app = APIGatewayRestResolver()


# List all todos in table
@app.get("/todos")
def list_todos():
    todos = todo_service.list()
    logger.info("list all todo request", todos=todos)
    return todos


# Create a new todo
@app.post("/todos")
def create_todo():
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    logger.info(todo_data)
    todo = todo_service.create(todo=todo_data)
    logger.info("create todo", todo=todo)
    return todo


# Retrieve a particular todo by by id
@app.get("/todos/<id>")
def get_todo_by_id(id):
    todo = todo_service.get(id=id)
    logger.info("retrieve todo", todo=todo)
    return todo


# Update a particular to todo by id
@app.put("/todos/<id>")
def update_todo(id):
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    logger.info(todo_data)
    todo = todo_service.update(todo={**todo_data, "id": id})
    logger.info("update todo", todo=todo)
    return todo


# Delete a particular to todo by id
@app.delete("/todos/<id>")
def delete_todo(id):
    logger.info(f"Request from {id} received")
    data = todo_service.delete(id=id)
    logger.info(data)
    return data


def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
