import os
import logging
from uuid import uuid4
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette_prometheus import metrics, PrometheusMiddleware
from starlette.staticfiles import StaticFiles

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

logging.config.fileConfig(logger_conf_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

# =================
# Setup API Router
# =================
app = FastAPI()

# force redirect of HTTP requests to HTTPS receiver
app.add_middleware(HTTPSRedirectMiddleware)

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
# Serving Static HTML - The Lazy Way
# ===================================
# mounts a completely indepedent application at the URI path /static
# subpaths of /static are mapped to files in the "static" directory
# so if '$APP_DIR/static/sample.html' is a valid filepath on the webhost, 
# then '$HOST:$PORT/static/sample.html' becomes the URI path
app.mount("/static", StaticFiles(directory="static"), name="static", html=True)

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