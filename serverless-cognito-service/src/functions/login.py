import json
import boto3
from botocore.config import Config
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder 
import logging

@xray_recorder.capture('login')
@cors_headers
def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    client = boto3.client('cognito-idp')
    req_body = json.loads(event['body'])
    username = req_body['username']
    password = req_body['password']

    resp = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            # 'SECRET_HASH': get_secret_hash(username),
            'PASSWORD': password,
        })

    logger.info(f"Login: {username}")

    return {
        "statusCode": 200,
        "body": json.dumps(resp["AuthenticationResult"])
    }
