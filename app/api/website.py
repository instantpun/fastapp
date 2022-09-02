import os
import logging
import logging.config
import pythonjsonlogger

from uuid import uuid4
import time

from typing import Union, List

from fastapi import FastAPI, Request, Response, UploadFile, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from starlette_prometheus import metrics, PrometheusMiddleware
# from starlette.staticfiles import StaticFiles

from pydantic import BaseModel

import pythonjsonlogger

# =================
# Log Setup
# =================
# If this app runs inside a container, shell variables are useful 
# for passing through configuration paramters
if os.environ.get('LOG_CONF_PATH'):
    logger_conf_path = os.environ.get('LOG_CONF_PATH')
else:
    logger_conf_path = './logging.conf'

if os.environ.get('LOG_LEVEL'):
    log_level = os.environ.get('LOG_LEVEL').upper()
else:
    log_level = 'INFO'

print(logger_conf_path)
logging.config.fileConfig(logger_conf_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

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

# =================
# Setup API Router
# =================
app = FastAPI()

# force redirect of HTTP requests to HTTPS receiver
app.add_middleware(HTTPSRedirectMiddleware)


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

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
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

@app.get("/oauth2-sample/")
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
# @app.get("/")
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

# @app.post("/upload/")
# async def create_upload_file(file: Union[UploadFile, None] = None) -> dict:
#     if not file:
#         # do what?
#     else:
#         # do else?

# @app.post("/upload/")
# async def create_upload_files(files: List[UploadFile]):
#     return {"filenames": [file.filename for file in files]}

# ================
# Monitoring 
# ================
# PrometheusMiddleware is a utility which wraps http request handlers and exports basic metrics
# add_route() configures the ASGI router to expose the metric stream at a valid URI path
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# =========================
# Custom Logging Middleware
# =========================
@app.middleware("http") 
async def log_requests(request: Request, call_next) -> Response:
    """  Wraps the call_next() request handler
    Args:
        request (starlette.Request): [description]
        call_next (starlette.middleware.BaseHTTPMiddleware.call_next): [description]
    Returns:
        response (starlette.Response): [description]
    """    
    request_id = str(uuid4()) # generate random uuid for log tracing
    extra_fields = {
        "request_id":request_id, 
        "path": request.url.path
        }
    logger.info("start request", extra=extra_fields)
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{:.2f}'.format(process_time) # millisecond with float precision of 2 digits
    extra_fields.update({ 
        "process_time_ms": formatted_process_time, 
        "status_code": response.status_code
        })
    logger.info("end request", extra=extra_fields)
    return response

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



# ===================================
# Serving Static HTML - The Lazy Way
# ===================================
# mounts a completely indepedent application at the URI path /static
# subpaths of /static are mapped to files in the "static" directory
# so if '$APP_DIR/static/sample.html' is a valid filepath on the webhost, 
# then '$HOST:$PORT/static/sample.html' becomes the URI path
# app.mount("/static", StaticFiles(directory="static"), name="static", html=True)

# =====================================
# Serving Static HTML - The Manual Way
# =====================================
# import pathlib
# current_dir = pathlib.Path(__file__).parent.resolve()
# @app.get("/")
# def read_root():
#     with open(f"{current_dir}/hello.html", "r") as f:
#         response = f.read()
#     if isinstance(response, bytes):
#         reponse = response.decode("utf-8")
#     return response