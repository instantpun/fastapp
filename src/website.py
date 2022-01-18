from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware
from starlette.staticfiles import StaticFiles

app = FastAPI()

# ===============
# Prometheus Setup
# ===============
# PrometheusMiddleware is a utility which wraps http request handlers and exports basic metrics
# add_route() configures the ASGI router to expose the metric stream at a valid URI path
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py
# Metrics Available:
# * starlette_requests_total
# * starlette_responses_total
# * starlette_requests_processing_time_seconds
# * starlette_exceptions_total
# * starlette_requests_in_progress

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

