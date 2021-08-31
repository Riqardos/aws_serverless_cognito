from aws_xray_sdk.core import xray_recorder
from src.functions.modules.config import *


@xray_recorder.capture("refreshToken")
@cors_headers
def handler(req_body, client):
    refresh_token = req_body["refresh_token"]
    response = client.initiate_auth(
        ClientId=get_client_id(),
        AuthFlow="REFRESH_TOKEN_AUTH",
        AuthParameters={
            "REFRESH_TOKEN": refresh_token,
        },
    )

    logger.info(f"Refreshing token!")
    return {
        "statusCode": 200,
        "body": response["AuthenticationResult"],
    }
