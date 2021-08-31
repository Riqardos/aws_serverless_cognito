from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder


@xray_recorder.capture("confirmSignUp")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]
    code = req_body["code"]

    client.confirm_sign_up(
        ClientId=get_client_id(),
        Username=username,
        ConfirmationCode=code,
        ForceAliasCreation=False,
    )

    logger.info(f"Confirming signup: {username}")

    return {"statusCode": 200, "body": {"message": "SignUp confirmed!"}}
