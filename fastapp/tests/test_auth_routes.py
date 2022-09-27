import base64
from typing import Any
from fastapi.testclient import TestClient

from fastapp.main import app

client = TestClient(app=app, base_url = "https://testserver:8443")

positive_tests = []
negative_tests = []

def test_auth_token_positive_01():
    """
    /auth/token expects a OAuth2-compliant form to be sent, 
    and returns a valid token.
    Operation:
    (1) Create mock form data that follows the OAuth2 spec
    (2) POST form data to token endpoint
        - VALID username
        - VALID password
        - VALID grant_type
        - VALID scope
    
    Expected Result:
    (1) HTTP 200 response
    (2) /auth/token function should return OAuth2-compliant JSON containing the token
    """
    form_data = {
        "username": "johndoe", 
        "password": "secret", 
        "scope": "sample01",
        "grant_type": "password"
        }
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "johndoe",
        "token_type": "bearer",
    }
    
    return response.json()

def test_auth_token_positive_02():
    """
    /auth/token expects a OAuth2-compliant form to be sent, 
    and returns a valid token.
    Operation:
    (1) Create mock form data that follows the OAuth2 spec
    (2) POST form data to token endpoint
        - VALID username
        - VALID password
        - VALID grant_type
        - VALID client_id
        - VALID client_secret
    
    Expected Result:
    (1) HTTP 200 response
    (2) /auth/token function should return OAuth2-compliant JSON containing the token
    """
    form_data = {
        "username": "johndoe", 
        "password": "secret", 
        "scope": "sample01",
        "grant_type": "password", 
        "client_id": "12345", 
        "client_secret": "somesecret"
        }
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "johndoe",
        "token_type": "bearer",
    }
    
    return response.json()

def test_auth_token_negative_01():
    """
    /auth/token expects a OAuth2-compliant form to be sent, 
    and returns a valid token.
    Operation:
    (1) Create mock form data that follows the OAuth2 spec
    (2) POST form data to token endpoint
        - INVALID username
        - VALID password
        - VALID grant_type
    
    Expected Result:
    (1) HTTP 400 response
    (2) /auth/token function should return OAuth2-compliant JSON containing a error message
    """
    form_data = {
        "username": "johndoe_invalid", 
        "password": "secret", 
        "grant_type": "password"
        }
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Incorrect username or password",
    }
    
    return response.json()


def test_auth_token_negative_02():
    """
    /auth/token expects a OAuth2-compliant form to be sent, 
    and returns a valid token.
    Operation:
    (1) Create mock form data that follows the OAuth2 spec
    (2) POST form data to token endpoint
        - VALID username
        - INVALID password
        - VALID grant_type
    
    Expected Result:
    (1) HTTP 400 response
    (2) /auth/token function should return OAuth2-compliant JSON containing a error message
    """
    form_data = {
        "username": "johndoe", 
        "password": "secret_invalid", 
        "grant_type": "password"
        }
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Incorrect username or password",
    }
    
    return response.json()

def test_auth_token_negative_03():
    """
    /auth/token expects a OAuth2-compliant form to be sent, 
    and returns a valid token.
    Operation:
    (1) Create mock form data that follows the OAuth2 spec
    (2) POST form data to token endpoint
        - VALID username
        - VALID password
        - MISSING grant_type
    
    Expected Result:
    (1) HTTP 422 response (malformed request)
    (2) /auth/token function should return OAuth2-compliant JSON containing a error message
    """
    form_data = {
        "username": "johndoe", 
        "password": "secret"
        }
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 422
    # {'detail': [{'loc': ['body', 'grant_type'], 'msg': 'field required', 'type': 'value_error.missing'}]}
    # assert response.json() == {
    #     "detail": Any
    # }
    
    return response.json()

def test_auth_user_me(auth_token_reponse=None):
    """

    Args:
        auth_token_reponse (_type_): _description_
    """
    resp = test_auth_token_positive_01()
    headers = {"Authorization": f"Bearer {resp['access_token']}"}
    user_resp = client.get("/auth/users/me", headers=headers, verify=True, cert='../fastapi-app.crt')
    
    
    assert user_resp.status_code == 200
    assert user_resp.json() is not None
    user_resp_json = user_resp.json()
    assert user_resp_json["username"] == "johndoe"
    assert user_resp_json["disabled"] == False