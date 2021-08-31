from aws_xray_sdk.core import xray_recorder
from src.functions.modules.config import *


@xray_recorder.capture("forgotPassword")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]

    response = client.forgot_password(ClientId=get_client_id(), Username=username)

    logger.info(f"Forgot password: {username}")
    return {
        "statusCode": 200,
        "body": response["CodeDeliveryDetails"],
    }
