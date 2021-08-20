import base64
import hashlib
import hmac
import json
import boto3
import botocore.exceptions

from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder 
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
@xray_recorder.capture('signUp')
@cors_headers
def lambda_handler(event, context):
    event = json.loads(event['body'])
    username = event['username']
    email = event["email"]
    password = event['password']
    client = boto3.client('cognito-idp')
    resp = client.sign_up(
        ClientId=CLIENT_ID,
        # SecretHash=get_secret_hash(username),
        Username=username,
        Password=password,
        UserAttributes=[
            {
                'Name': "email",
                'Value': email
            }
        ],
        ValidationData=[
            {
                'Name': "email",
                'Value': email
            }
        ])

        
    logger.info(f"Signup: {username}")

    return {
        "statusCode": 201,
        "body": "Please confirm your signup, check Email for validation code",
    }
