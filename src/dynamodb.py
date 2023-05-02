import boto3


class DynamodbClient:
    def __init__(self, table_name: str) -> None:
        self._client = boto3.client("dynamodb")
        self._table_name = table_name

    def query(self) -> list:
        response = self._client.query(
            TableName=self._table_name,
            KeyConditionExpression="",
        )
        return response.Items

    def put_item(self, item) -> list:
        self._client.put_item(
            TableName=self._table_name,
            Item={
                "id": {
                    "S": item.id
                },
                "content": {
                    "S": item.content
                }
            }
        )
