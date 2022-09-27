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
`uvicorn main:app --host 0.0.0.0 --port 8080 --reload --log-config logging.conf`

For HTTP/2 Support use:
`hypercorn --bind 0.0.0.0:8000 main:app --log-config logging.conf`

`hypercorn --certfile fastapi-app.crt --keyfile fastapi-app.key --bind localhost:8443 --insecure-bind localhost:8080 main:app --access-logformat ''`

Create Self-signed Cert & Private Key

```
openssl req \
       -newkey rsa:2048 -nodes -keyout fastapi-app.key \
       -x509 -days 365 -out fastapi-app.crt
```

podman pod create --replace \
--name fastapi \
--network podman \
-p 38000:8000 \
-p 38080:8080 \
-p 38443:8443

podman run -it --replace \
--network slirp4netns:port_handler=slirp4netns
--name sample1 \
--pod fastapi \
fastapi:demo-v1

```
for IMAGE in $(docker images | awk '{ print $3}'); do
docker rmi $IMAGE; done
```

```
for ARN in $(aws resourcegroupstaggingapi get-resources --tag-filters=Key=Application,Values=demo-fastapi | jq -r '.ResourceTagMappingList[] | .ResourceARN'); do 
```