# Std Libs
import os
# import logging
# import logging.config

from typing import Union, List

# 3rd Party Packages
import pythonjsonlogger


from fastapi import APIRouter, Request, Response, UploadFile, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, OAuth2PasswordRequestFormStrict
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

# ====================
# Data Models
# ====================
class User(BaseModel):
    username: str
    email: Union[str, None] = None 
    full_name: Union[str, None] = None 
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}




# @app.on_event("startup")
# async def startup_event():
#     logger = logging.getLogger("uvicorn.access")
#     handler = logging.StreamHandler()
#     handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
#     logger.addHandler(handler)
    
# ===========================
# OIDC/OAuth2 Security Setup
# ===========================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ================================
# OIDC/OAuth2 Helper Functions
# ================================

def fake_hash_password(password: str) -> str:
    return "fakehashed" + password

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# ================
# Path Operations
# ================

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestFormStrict = Depends()):
    
    # fetch user record from fake DB by username
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    
    # received hash should match hash in fake DB
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)) -> User:
    """_summary_

    Args:
        current_user (User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        User: _description_
    """
    return current_user
    
# From the FastApi Docs:
# All the security utilities that integrate with OpenAPI 
# (and the automatic API docs) inherit from SecurityBase (including OAuth2PasswordBearer), 
# that's how FastAPI can know how to integrate them in OpenAPI.
# 
# `Depends(oauth2_scheme)`
# Depends() declares oauth2_scheme (class: OAuth2PasswordBearer) as a dependency,
# so FastApi will automatically add a new "security scheme" to the OpenAPI schema 

@router.get("/oauth2-sample/")
async def read_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    read_token() will go and look in the request for that Authorization header, 
    check if the value is Bearer plus some token, and will return the token as a str.
    If it doesn't see an Authorization header, or the value doesn't have a Bearer token, 
    it will respond with a 401 status code error (UNAUTHORIZED) directly.
    Depends() always returns a string, so the token will never be None.

    Args:
        token (str, optional): _description_. Defaults to Depends(oauth2_scheme).

    Returns:
        dict: contains the OAuth2 token retrieved from the Authorization header
    
    
    """
    return {"token": token}


# ================
# Path Operations
# ================
# @app.get("/login")
# async def main():
#     content = """
# <body>
# <form action="/upload/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)

# ===================================
# Custom Router Dependencies
# ===================================
# You might be asking, "But why?"
# It is generally considered bad practice to consume the request 
# object within middleware of any kind, but sometimes you need to.
# 
# In Starlette (and FastAPI), the way json is "cached" inside the 
# starlette Request means the cached json is NOT transferred to 
# the next called asgi app.
# So, something like print(await request.json()) inside middleware causes a crash
# See: https://github.com/tiangolo/fastapi/issues/394
#
# ```app.include_router(api_router, dependencies=[Depends(wrapperFunc)])```
# 
# This requires you to add all endpoints to api_router rather than app, but 
# ensures that wrapperFunc will be called for every endpoint added to it 
# (functioning very similarly to a middleware, given that all endpoints pass 
# through api_router).

