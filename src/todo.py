from uuid import uuid4

from dynamodb import DynamodbClient

TODOS_TABLE = "todos"
ddb_client = DynamodbClient(table_name=TODOS_TABLE)


class TodoService:
    def __init__(self):
        pass

    def list(self) -> list:
        return ddb_client.scan()

    def get(self, id) -> dict:
        return ddb_client.get_item(id=id)

    def create(self, todo) -> dict:
        item = {"id": str(uuid4()), "completed": "false", **todo}
        return ddb_client.put_item(item)

    def update(self, todo) -> dict:
        return ddb_client.update_item(item=todo)

    def delete(self, id) -> dict:
        return ddb_client.delete_item(id=id)
