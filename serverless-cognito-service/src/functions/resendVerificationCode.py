from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder


@xray_recorder.capture("resendVerification")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]
    client.resend_confirmation_code(
        ClientId=get_client_id(),
        Username=username,
    )
    logger.info(f"User {username} is resending verification code!")

    return {
        "statusCode": 200,
        "body": {"message": f"User: {username} is resending verification code!"},
    }
