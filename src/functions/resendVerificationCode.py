import json
import boto3
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder

@xray_recorder.capture('resendVerification')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    username = json.loads(event['body'])['username']
    response = client.resend_confirmation_code(
        ClientId=CLIENT_ID,
        # SecretHash=get_secret_hash(username),
        Username=username,
    )

    return {"statusCode": 200, "body": "OK"}


if __name__ == "__main__":
    print(lambda_handler({
        "username": "test2",
    }, "test"))
