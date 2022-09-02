# Std Libs
import os
import logging
import logging.config
from uuid import uuid4
import time

# 3rd Party Packages
from fastapi import FastAPI, Request, Response
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette_prometheus import metrics, PrometheusMiddleware

# Local Modules
# import api

# import uvicorn
# uvicorn.run("main.api:app", port=5000, reload=True, access_log=False)


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

# =================
# Setup API Router
# =================
app = FastAPI()

# force redirect of HTTP requests to HTTPS receiver
# app.add_middleware(HTTPSRedirectMiddleware)

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

# =========================
# Add Routes
# =========================
from fastapp.routers import auth
app.include_router(auth.router)
# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
