import json
import boto3
import pytest
from moto import XRaySegment, mock_cognitoidp, mock_ssm, mock_xray_client
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "../..")

from src.functions.login import handler as login_handler
from src.functions.signUp import handler as sign_up_handler
from src.functions.confirmSignUp import handler as confirm_sign_up_handler
from src.functions.refreshToken import handler as refresh_token_handler
from src.functions.resendVerificationCode import handler as resend_code_handler
from src.functions.forgotPassword import handler as forgot_password_handler
from src.functions.listUsers import handler as list_users_handler
from src.functions.confirmForgotPassword import handler as confirm_forgot_password_handler
from src.functions.modules.config import *



@pytest.fixture
def create_cognito_ssm():
    @mock_cognitoidp
    @mock_ssm
    @mock_xray_client
    def boto_resource():
        ssm_client = boto3.client("ssm")
        cognito_client = boto3.client("cognito-idp")

        cognito_res = cognito_client.create_user_pool(
            PoolName="test_pool", AutoVerifiedAttributes=["email"]
        )
        user_pool_id = cognito_res["UserPool"]["Id"]

        cognito_client_res = cognito_client.create_user_pool_client(
            UserPoolId=user_pool_id, ClientName="test_client"
        )

        ssm_client.put_parameter(
            Name="/rk-cognito-sls/clientAppId",
            Value=cognito_client_res["UserPoolClient"]["ClientId"],
        )

        ssm_client.put_parameter(
            Name="/rk-cognito-sls/cognitoUserPoolId", Value=user_pool_id
        )

        cognito_client.sign_up(
            ClientId=get_client_id(),
            Username="UnconfirmedUser",
            Password="Testicek123!",
            UserAttributes=[{"Name": "email", "Value": "test@test.com"}],
            ValidationData=[{"Name": "email", "Value": "test@test.com"}],
        )

        cognito_client.sign_up(
            ClientId=get_client_id(),
            Username="ConfirmedUser",
            Password="Testicek123!",
            UserAttributes=[{"Name": "email", "Value": "test@test.com"}],
            ValidationData=[{"Name": "email", "Value": "test@test.com"}],
        )

        # not implemneted in moto see. https://github.com/spulec/moto/blob/master/IMPLEMENTATION_COVERAGE.md
        # unable to confirm registration
        # cognito_client.admin_confirm_sign_up(
        #     UserPoolId=user_pool,
        #     Username="ConfirmedUser"
        # )

        # this confirmation works somehow, without valid confirmation code
        cognito_client.confirm_sign_up(
            ClientId=get_client_id(),
            Username="ConfirmedUser",
            ConfirmationCode="12345",
            ForceAliasCreation=False,
        )

    return boto_resource


def add_xray_segment(function):
    def wrapper(*args, **kwargs):
        with XRaySegment():
            return function(*args, **kwargs)
    
    return wrapper

def add_cognito_fixture(function):
    def wrapper(create_cognito_ssm, *args, **kwargs):
        create_cognito_ssm()
        return function(*args, **kwargs)

    return wrapper

@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_login_username_doesnt_exists():
    res = login_handler(
        {"body": json.dumps({"username": "test", "password": "test"})}, {}
    )
    assert json.loads(res["body"])["error"] == "Username doesnt exists!"


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_login_username_wrong_password():
    res = login_handler(
        {"body": json.dumps({"username": "ConfirmedUser", "password": "test"})}, {}
    )
    assert json.loads(res["body"])["error"] == "The username or password is incorrect!"


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_login_user_unconfirmed():

    res = login_handler(
        {
            "body": json.dumps(
                {"username": "UnconfirmedUser", "password": "Testicek123!"}
            )
        },
        {},
    )
    assert json.loads(res["body"])["error"] == "User is not confirmed!"

@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_login_user_confirmed():
    res = login_handler(
        {"body": json.dumps({"username": "ConfirmedUser", "password": "Testicek123!"})},
        {},
    )
    assert json.loads(res["body"])["AccessToken"]


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_sign_up_username_exists():
    res = sign_up_handler(
        {
            "body": json.dumps(
                {
                    "username": "ConfirmedUser",
                    "password": "Testicek123!",
                    "email": "test@test.com",
                }
            )
        },
        {},
    )
    assert json.loads(res["body"])["error"] == "This username already exists!"


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_sign_up_confirm_new_user():
    res = sign_up_handler(
        {
            "body": json.dumps(
                {
                    "username": "testtest",
                    "password": "Testicek123!",
                    "email": "test@test.com",
                }
            )
        },
        {},
    )
    assert (
        json.loads(res["body"])["message"]
        == "Please confirm your signup, check Email for validation code!"
    )


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_sign_up_confirm():
    res = confirm_sign_up_handler(
        {"body": json.dumps({"username": "UnconfirmedUser", "code": "12345"})}, {}
    )

    assert json.loads(res["body"])["message"] == "SignUp confirmed!"

    res = confirm_sign_up_handler(
        {"body": json.dumps({"username": "NotExistUser", "code": "12345"})}, {}
    )

    assert json.loads(res["body"])["error"] == "Username doesnt exists!"

@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_refresh_token():
    res = login_handler(
        {"body": json.dumps({"username": "ConfirmedUser", "password": "Testicek123!"})},
        {},
    )
    refresh_token =  json.loads(res["body"])["RefreshToken"]


    res = refresh_token_handler({"body": json.dumps({
        "refresh_token": refresh_token,
    })}, {})

    assert json.loads(res['body'])['AccessToken']

@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_list_users():

    res = list_users_handler({}, {})

    assert json.loads(res["body"])[0]["Username"] == "UnconfirmedUser"


@mock_cognitoidp
@add_cognito_fixture
@add_xray_segment
def test_forgot_password_correct_code():

    res = forgot_password_handler(
        {
            "body": json.dumps(
                {
                    "username": "UnconfirmedUser",
                }
            )
        },
        {},
    )

    assert json.loads(res["body"])["DeliveryMedium"] == "EMAIL"

    res = confirm_forgot_password_handler(
        {
            "body": json.dumps(
                {
                    "username": "UnconfirmedUser",
                    "code": "12345",
                    "password": "newPassword123!",
                }
            )
        },
        {},
    )

    assert json.loads(res["body"])["message"] == "Password confirmed!"

@pytest.mark.skip(reason="moto returns OK on every code verification")
def test_forgot_password_wrong_code():
    pass

@pytest.mark.skip(reason="not implemented in moto")
def test_resend_confirmation_code():
    # not implemented in moto see https://github.com/spulec/moto/blob/master/IMPLEMENTATION_COVERAGE.md
    pass