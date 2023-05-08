import boto3


class DynamodbClient:
    def __init__(self, table_name: str) -> None:
        self._client = boto3.client("dynamodb")
        self._dynomodb = boto3.resource("dynamodb", region_name="cn-north-1")
        self._table = self._dynomodb.Table(table_name)

    def scan(self) -> list:
        response = self._table.scan()
        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self._table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return data

    def get_item(self, id: str) -> dict:
        response = self._table.get_item(Key={"id": id})
        return response["Item"]

    def put_item(self, item: dict) -> dict:
        response = self._table.put_item(Item=item)
        return response["Attributes"]

    def update_item(self, item: dict) -> dict:
        print(item)
        response = self._table.update_item(
            Key={"id": item["id"]},
            UpdateExpression="set #completed = :completed",
            ExpressionAttributeNames={"#completed": "completed"},
            ExpressionAttributeValues={":completed": item["completed"]},
            ReturnValues="UPDATED_NEW",
        )
        return response["Attributes"]

    def delete_item(self, id: str) -> None:
        response = self._table.delete_item(Key={"id": id}, ReturnValues="ALL_OLD")
        return response["Attributes"]
