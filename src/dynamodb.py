import boto3
from boto3.dynamodb.conditions import Attr


class DynamodbClient:
    def __init__(self, table_name: str) -> None:
        self._client = boto3.client("dynamodb")
        self._dynomodb = boto3.resource("dynamodb", region_name="cn-north-1")
        self._table = self._dynomodb.Table(table_name)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/scan.html
    def scan(self) -> list:
        response = self._table.scan()
        data = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self._table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            data.extend(response["Items"])
        return data

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/get_item.html
    def get_item(self, id: str) -> dict:
        response = self._table.get_item(Key={"id": id})
        return response["Item"]

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/put_item.html
    def put_item(self, item: dict) -> None:
        self._table.put_item(Item=item)

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/update_item.html
    def update_item(self, item: dict) -> dict:
        id = item["id"]
        response = self._table.update_item(
            Key={"id": id},
            UpdateExpression="set #completed = :completed",
            ExpressionAttributeNames={"#completed": "completed"},
            ExpressionAttributeValues={":completed": item["completed"]},
            ConditionExpression=Attr("id").eq(id),
            ReturnValues="UPDATED_NEW",
        )
        return response["Attributes"]

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/table/delete_item.html
    def delete_item(self, id: str) -> None:
        response = self._table.delete_item(
            Key={"id": id},
            ReturnValues="ALL_OLD",
            ConditionExpression=Attr("id").eq(id),
        )
        return response["Attributes"]
