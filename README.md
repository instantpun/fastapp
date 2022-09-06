# FastApp Demo Website

## Getting started

Setup coding env:

Setup fresh virtual environment:
`python3 -m venv venv`

Activate virtual environment:
`source venv/bin/activate`

Install prereqs:
`python3 -m pip install -r requirements.txt`

Enable package-based imports:
`python3 -m pip install -e <dir_containing_setup.py>`



Start basic server with:
`uvicorn api.website:app --host 0.0.0.0 --port 8000 --reload --log-config logging.conf`

For HTTP/2 Support use:
`hypercorn --bind 0.0.0.0:8000 api.website:app --log-config logging.conf`

`hypercorn --certfile fastapi-app.crt --keyfile fastapi-app.key --bind localhost:8443 --insecure-bind localhost:8080 fastapp.__main__:APP --access-logformat ''`

Create Self-signed Cert & Private Key

```
openssl req \
       -newkey rsa:2048 -nodes -keyout fastapi-app.key \
       -x509 -days 365 -out fastapi-app.crt
```

## Metrics
This website uses Prometheus to expose metrics. The `starlette-prometheus` module provides a wrapper for HTTP handlers managed by Starlette and exposes common web metrics.

```app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)```

https://github.com/perdy/starlette-prometheus/blob/master/starlette_prometheus/middleware.py

Metrics Available:
* starlette_requests_total
* starlette_responses_total
* starlette_requests_processing_time_seconds
* starlette_exceptions_total
* starlette_requests_in_progress



