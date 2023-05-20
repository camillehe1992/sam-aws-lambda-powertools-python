from uuid import uuid4
from aws_lambda_powertools import Logger
from dynamodb import DynamodbClient

TODOS_TABLE = "todos"
ddb_client = DynamodbClient(table_name=TODOS_TABLE)

logger = Logger(service="TodoService")


class TodoService:
    def __init__(self):
        pass

    def list(self) -> list:
        try:
            todos = ddb_client.scan()
            message = "list all todos successfully"
            logger.info(message, todos=todos)
            return {"message": message, "todos": todos}
        except Exception as e:
            logger.error("failed to list todos", error=e)
            raise e

    def get(self, id) -> dict:
        try:
            todo = ddb_client.get_item(id=id)
            message = "retrieve todo successfully"
            logger.info(message, todo=todo)
            return {"message": message, "todo": todo}
        except Exception as e:
            logger.error(f"failed to retrieve todo {id}")
            raise e

    def create(self, todo_data) -> dict:
        try:
            item = {**todo_data, "id": str(uuid4()), "completed": "false"}
            ddb_client.put_item(item=item)
            message = "create todo successfully"
            logger.info(message, todo=item)
            return {"message": message, "todo": item}
        except Exception as e:
            logger.error("failed to create todo")
            raise e

    def update(self, todo_data) -> dict:
        try:
            todo = ddb_client.update_item(item=todo_data)
            message = "update todo successfully"
            logger.info(message, todo=todo)
            return {"message": message, "todo": todo}
        except Exception as e:
            logger.error("failed to update todo", todo=todo_data)
            raise e

    def delete(self, id) -> dict:
        try:
            todo = ddb_client.delete_item(id=id)
            message = "delete todo successfully"
            logger.info(message, todo=todo)
            return {"message": message, "todo": todo}
        except Exception as e:
            logger.error(f"failed to delete todo {id}")
            raise e
