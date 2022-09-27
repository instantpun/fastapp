# Std Libs
import os

# 3rd Party Packages
#import pythonjsonlogger

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

router = APIRouter(
    tags=["static"],
    responses={404: {"description": "Not found"}},
)

# ===================================
# Serving Static HTML - The Lazy Way
# ===================================
# mounts a completely indepedent application at the URI path /static
# subpaths of /static are mapped to files in the "static" directory
# so if '$APP_DIR/static/sample.html' is a valid filepath on the webhost, 
# then '$HOST:$PORT/static/sample.html' becomes the URI path
router.mount("/static", StaticFiles(directory="static"), name="static")#, html=True)

# =====================================
# Serving Static HTML - The Manual Way
# =====================================
# import pathlib
# current_dir = pathlib.Path(__file__).parent.resolve()
# @router.get("/")
# def read_root():
#     with open(f"{current_dir}/static/hello.html", "r") as f:
#         response = f.read()
#     if isinstance(response, bytes):
#         reponse = response.decode("utf-8")
#     return response