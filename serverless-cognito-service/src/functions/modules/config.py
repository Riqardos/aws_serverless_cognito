import base64
import datetime
import hashlib
import hmac
import json
import logging
import boto3
import jwt

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


def get_username_jwt(token):
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded["cognito:username"]


def get_parameter(name):
    def tmp():
        client = boto3.client("ssm")
        response = client.get_parameter(Name=name, WithDecryption=False)
        return response["Parameter"]["Value"]

    return tmp


get_client_id = get_parameter("/rk-cognito-sls/clientAppId")
get_user_pool_id = get_parameter("/rk-cognito-sls/cognitoUserPoolId")


def get_secret_hash(username):
    CLIENT_SECRET = get_parameter("/rk-cognito-sls/clientSecret")
    msg = username + get_client_id()
    dig = hmac.new(
        str(CLIENT_SECRET).encode("utf-8"),
        msg=str(msg).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def cors_headers(function):
    def wrapper(event, context, *args, **kwargs):

        try:
            req_body = json.loads(event["body"])
        except Exception as e:
            req_body = ""

        client = boto3.client("cognito-idp")

        headers = {
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            }
        }

        error = True
        try:
            response = function(req_body, client, *args, **kwargs)
            error = False
        except client.exceptions.NotAuthorizedException:
            response = {
                "statusCode": 401,
                "body": "The username or password is incorrect!",
            }
        except client.exceptions.UserNotConfirmedException:
            response = {"statusCode": 401, "body": "User is not confirmed!"}
        except client.exceptions.UsernameExistsException as e:
            response = {"statusCode": 401, "body": "This username already exists!"}
        except client.exceptions.UserNotFoundException:
            response = {"statusCode": 401, "body": "Username doesnt exists!"}
        except client.exceptions.InvalidParameterException:
            response = {"statusCode": 401, "body": "User is already confirmed!"}
        except client.exceptions.InvalidPasswordException as e:
            response = {
                "statusCode": 401,
                "body": "Password should have Caps,Special chars, Numbers!",
            }
        except client.exceptions.UserLambdaValidationException as e:
            response = {"statusCode": 401, "body": "Email already exists!"}
        except client.exceptions.CodeMismatchException:
            response = {"statusCode": 401, "body": "Invalid Verification code!"}
        except client.exceptions.NotAuthorizedException:
            response = {"statusCode": 401, "body": "User is already confirmed!"}
        except client.exceptions.ExpiredCodeException:
            response = {
                "statusCode": 401,
                "body": "Invalid code provided, please request a code again!",
            }
        except Exception as e:
            print(e)
            response = {"statusCode": 500, "body": str(e)}

        if error:
            logger.error(response["body"])
            return {
                **response,
                **headers,
                "body": json.dumps({"error": response["body"]}),
            }

        logger.info(response["body"])

        return {
            **response,
            **headers,
            "body": json.dumps(response["body"], default=default),
        }

    return wrapper
