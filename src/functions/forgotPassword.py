import json
import boto3
from aws_xray_sdk.core import xray_recorder
from botocore.config import Config
from src.functions.modules.config import *


@xray_recorder.capture('forgotPassword')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    req_body = json.loads(event['body'])
    username = req_body['username']

    resp = client.forgot_password(
        ClientId=CLIENT_ID,
        # SecretHash=get_secret_hash(username),
        Username=username
    )
    return {
        "statusCode": 200,
        "body": json.dumps(resp["CodeDeliveryDetails"])
    }
