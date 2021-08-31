from aws_xray_sdk.core import xray_recorder
from src.functions.modules.config import *


@xray_recorder.capture("confirmForgotPassword")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]
    code = req_body["code"]
    password = req_body["password"]

    client.confirm_forgot_password(
        ClientId=get_client_id(),
        ConfirmationCode=code,
        Username=username,
        Password=password,
    )

    logger.info(f"User {username} is confirming forgotten password")

    return {"statusCode": 200, "body": {"message": "Password confirmed!"}}
