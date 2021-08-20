import json
import boto3
from aws_xray_sdk.core import xray_recorder
from botocore.config import Config
from src.functions.modules.config import *
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
@xray_recorder.capture('refreshToken')
@cors_headers
def lambda_handler(event, context):
    client = boto3.client('cognito-idp')
    req_body = json.loads(event['body'])
    refresh_token = req_body['refresh_token']
    # username = req_body['username']

    resp = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            # 'SECRET_HASH': get_secret_hash(username),
            'REFRESH_TOKEN': refresh_token,
        })
    logger.info(f"Refreshing token")
    return {
        "statusCode": 200,
        "body": json.dumps(resp["AuthenticationResult"])
    }
