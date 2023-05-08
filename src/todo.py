from uuid import uuid4

from dynamodb import DynamodbClient

TODOS_TABLE = "todos"
ddb_client = DynamodbClient(table_name=TODOS_TABLE)


class TodoService:
    def __init__(self):
        pass

    def list(self) -> list:
        response = ddb_client.scan()
        return {"message": "list todos", "items": response["items"]}

    def get(self, id) -> dict:
        try:
            response = ddb_client.get_item(id=id)
            return {"message": "get todo", "items": response["item"]}
        except Exception as e:
            raise e

    def create(self, todo) -> dict:
        try:
            item = {"id": str(uuid4()), "completed": "false", **todo}
            ddb_client.put_item(item)
            return {"message": "todo created", "item": item}
        except Exception as e:
            raise e

    def update(self, todo) -> dict:
        try:
            response = ddb_client.update_item(item=todo)
            return {"message": f"todo updated", "item": response}
        except Exception as e:
            raise e

    def delete(self, id) -> dict:
        try:
            response = ddb_client.delete_item(id=id)
            return {"message": f"todo deleted", "item": response}
        except Exception as e:
            raise e
