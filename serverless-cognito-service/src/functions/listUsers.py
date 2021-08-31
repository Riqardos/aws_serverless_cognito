import datetime
from src.functions.modules.config import *
from aws_xray_sdk.core import xray_recorder

# Object of type datetime is not JSON serializable
def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


@xray_recorder.capture("listUsers")
@cors_headers
def handler(req_body, client):
    response = client.list_users(
        UserPoolId=get_user_pool_id(),
    )
    logger.info(f"Listing users")

    return {
        "statusCode": 200,
        "body": response["Users"],
    }
