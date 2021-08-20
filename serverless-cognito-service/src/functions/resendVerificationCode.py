import json
import boto3
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
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
    logger.info(f"Resending verification code: {username}")
    return {"statusCode": 200, "body": "OK"}


