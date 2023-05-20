from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit

from todo import TodoService

todo_service = TodoService()

logger = Logger(service="Todos")
tracer = Tracer(service="Todos")
metrics = Metrics(namespace="Todos", service="Todos")
app = APIGatewayRestResolver()


# List all todos in table
@app.get("/todos")
@tracer.capture_method
def list_todos():
    tracer.put_annotation(key="Todo", value="unknown")
    logger.info("List all todo request")
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    todos = todo_service.list()
    logger.info(f"todos: {todos}")
    return todos


# Create a new todo
@app.post("/todos")
@tracer.capture_method
def create_todo():
    tracer.put_annotation(key="Todo", value="unknown")
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    logger.info(f"todo_data: {todo_data}")
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    todo = todo_service.create(todo=todo_data)
    logger.info(f"todo: {todo}")
    return todo


# Retrieve a particular todo by by id
@app.get("/todos/<id>")
@tracer.capture_method
def get_todo_by_id(id):
    tracer.put_annotation(key="Todo", value=id)
    logger.info(f"Retrieve todo {id}")
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    todo = todo_service.get(id=id)
    logger.info(f"todo: {todo}")
    return todo


# Update a particular to todo by id
@app.put("/todos/<id>")
@tracer.capture_method
def update_todo(id):
    tracer.put_annotation(key="Todo", value=id)
    todo_data: dict = app.current_event.json_body  # deserialize json str to dict
    logger.info(f"todo_data: {todo_data}")
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    res = todo_service.update(todo={**todo_data, "id": id})
    logger.info(f"res: {res}")
    return res


# Delete a particular to todo by id
@app.delete("/todos/<id>")
@tracer.capture_method
def delete_todo(id):
    tracer.put_annotation(key="Todo", value=id)
    logger.info(f"Request from {id} received")
    metrics.add_metric(name="SuccessfulGreetings", unit=MetricUnit.Count, value=1)
    res = todo_service.delete(id=id)
    logger.info(f"res: {res}")
    return res


@tracer.capture_lambda_handler
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True
)
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event, context):
    try:
        return app.resolve(event, context)
    except Exception as e:
        logger.exception(e)
        raise
