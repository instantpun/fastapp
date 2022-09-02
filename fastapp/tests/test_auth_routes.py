import base64
from fastapi.testclient import TestClient

from fastapp.main import app

client = TestClient(app=app, base_url = "https://testserver:8443")


def test_auth_token():
    form_data = {"username": "johndoe", "password": "secret"}
    response = client.post("/auth/token", data=form_data, verify=True, cert='../fastapi-app.crt')

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "johndoe",
        "token_type": "bearer",
    }
    
    return response.json()
    
def test_auth_user_me():
    resp = test_auth_token()
    headers = {"Authorization": f"Bearer {resp['access_token']}"}
    user_resp = client.get("/auth/users/me", headers=headers, verify=True, cert='../fastapi-app.crt')
    
    
    assert user_resp.status_code == 200
    assert user_resp.json() is not None
    user_resp_json = user_resp.json()
    assert user_resp_json["username"] == "johndoe"
    assert user_resp_json["disabled"] == False