from aws_xray_sdk.core import xray_recorder
from src.functions.modules.config import *


@xray_recorder.capture("signUp")
@cors_headers
def handler(req_body, client):
    username = req_body["username"]
    email = req_body["email"]
    password = req_body["password"]
    client.sign_up(
        ClientId=get_client_id(),
        Username=username,
        Password=password,
        UserAttributes=[{"Name": "email", "Value": email}],
        ValidationData=[{"Name": "email", "Value": email}],
    )

    logger.info(f"User: {username} is singing up!")

    return {
        "statusCode": 201,
        "body": {
            "message": "Please confirm your signup, check Email for validation code!"
        },
    }
