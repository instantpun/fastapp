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


## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

