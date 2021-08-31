from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core.recorder import AWSXRayRecorder
from src.functions.modules.config import *


@xray_recorder.capture("login")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]
    password = req_body["password"]

    response = client.initiate_auth(
        ClientId=get_client_id(),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password,
        },
    )

    logger.info(f"{username} has logged in successfully!")

    return {
        "statusCode": 200,
        "body": response["AuthenticationResult"],
    }
