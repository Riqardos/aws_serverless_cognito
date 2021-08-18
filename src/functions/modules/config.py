import base64
import hashlib
import hmac
import json

import boto3

CLIENT_SECRET = 'mmnnon82301q2f4ieovs2la34k1edm6h944igrlnh9t8gme8sff'

def get_parameter(name):
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name=name,
        WithDecryption=False
    )
    return response['Parameter']['Value']

CLIENT_ID = get_parameter('/rk-cognito-sls/clientAppId')
USER_POOL_ID = get_parameter('/rk-cognito-sls/cognitoUserPoolId')

def get_secret_hash(username):
    msg = username + CLIENT_ID
    dig = hmac.new(str(CLIENT_SECRET).encode(
        'utf-8'), msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2

def cors_headers(function):
    def wrapper(*args, **kwargs):
        client = boto3.client('cognito-idp')
        cors_header = {
            'headers': {
                "Content-Type": "application/json",
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            }
        }
        try:
            response = function(*args, **kwargs)
        except client.exceptions.NotAuthorizedException:
            response = {"statusCode": 401,
                        "body": "The username or password is incorrect"}
        except client.exceptions.UserNotConfirmedException:
            response = {"statusCode": 401, "body": "User is not confirmed"}
        except client.exceptions.UsernameExistsException as e:
            response = {"statusCode": 401,
                        "body": "This username already exists"}
        except client.exceptions.UserNotFoundException:
            response = {"statusCode": 401, "body":   "Username doesnt exists"}
        except client.exceptions.InvalidParameterException:
            response = {"statusCode": 401, "body": "User is already confirmed"}
        except client.exceptions.InvalidPasswordException as e:
            response = {"statusCode": 401,
                        "body": "Password should have Caps,Special chars, Numbers"}
        except client.exceptions.UserLambdaValidationException as e:
            response = {"statusCode": 401, "body": "Email already exists"}
        except client.exceptions.UserNotFoundException:
            response = {"statusCode": 401, "body": "Username doesnt exists"}
        except client.exceptions.CodeMismatchException:
            response = {"statusCode": 401, "body": "Invalid Verification code"}
        except client.exceptions.NotAuthorizedException:
            response = {"statusCode": 401, "body": "User is already confirmed"}
        except client.exceptions.ExpiredCodeException:
            response = {
                "statusCode": 401, "body": "Invalid code provided, please request a code again."}
        except Exception as e:
            response = {"statusCode": 500, "body": str(e)}

        return {
            **response,
            **cors_header
        }

    return wrapper
