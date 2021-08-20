import json
import boto3
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


@xray_recorder.capture('confirmSignUp')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    event = json.loads(event['body'])
    username = event['username']
    code = event['code']
    response = client.confirm_sign_up(
        ClientId=CLIENT_ID,
        # SecretHash=get_secret_hash(username),
        Username=username,
        ConfirmationCode=code,
        ForceAliasCreation=False,
    )

    logger.info(f"Confirming signup: {username}")

    return {"statusCode": 200, "body": f"{response} "}
