import datetime
import json
import boto3
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder

# Object of type datetime is not JSON serializable
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

@xray_recorder.capture('listUsers')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    resp = client.list_users(
        UserPoolId=USER_POOL_ID,
    )
    return {
        "statusCode": 200,
        "body": json.dumps(resp["Users"], default=default)
    }



if __name__ == "__main__":
    print(lambda_handler("test", "test"))
