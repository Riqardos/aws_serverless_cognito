import json
import boto3
from aws_xray_sdk.core import xray_recorder
from botocore.config import Config
from src.functions.modules.config import *


@xray_recorder.capture('confirmForgotPassword')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    req_body = json.loads(event['body'])
    username = req_body['username']
    code = req_body['code']
    password = req_body['password']

    resp = client.confirm_forgot_password(
        ClientId=CLIENT_ID,
        # SecretHash=get_secret_hash(username),
        ConfirmationCode=code,
        Username=username,
        Password=password,
    )
    return {
        "statusCode": 200,
        "body": json.dumps(resp)
    }
