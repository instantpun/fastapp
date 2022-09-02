# Using LTS Ubuntu Focal
FROM docker.io/ubuntu:22.04

ENV ARCH=amd64 \
    PYTHON_VERSION=3.10.4

RUN apt update && \
    apt install -y curl gpg unzip libdigest-sha-perl build-essential \
    zlib1g zlib1g-dev libncurses5-dev libssl-dev libreadline-dev libffi-dev wget

# B26995E310250568 is the current gpg key ID for python
#RUN curl -OsL "https://keybase.io/pablogsal/pgp_keys.asc?fingerprint=a035c8c19219ba821ecea86b64e628f8d684696d" | gpg --import - && \
RUN cd /tmp && \
    curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x64E628F8D684696D" | gpg --import - && \
    curl -OsL "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" && \
    curl -OsL "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz.asc" && \
    gpg --verify Python-${PYTHON_VERSION}.tgz.asc Python-${PYTHON_VERSION}.tgz && \
    if [ $? -ne 0 ]; then exit 1; fi && \
    tar -xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION}  && \
    chmod +x ./configure && ./configure --enable-optimizations && \
    make altinstall && \
    SHORT_VERSION=$(echo ${PYTHON_VERSION} | cut -d . -f 1,2) && \
    ln -s /usr/local/bin/python${SHORT_VERSION} /usr/local/bin/python3 && \
    cd / && rm -rf /tmp/Python.*

ENV HOME="/home/app"

RUN useradd -m -d "${HOME}" -s /bin/bash app

WORKDIR /home/app

COPY --chown=app app/ /home/app

RUN python3 -m pip install -r "${HOME}/requirements.txt"

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

USER app:app

ENV LOG_CONF_PATH="${HOME}/logging.conf"

ENTRYPOINT ["/tini", "--"]

CMD ["hypercorn", "--certfile", "fastapi-app.crt", "--keyfile", "fastapi-app.key", "--bind", "localhost:8443", "--insecure-bind", "localhost:8080", "api.website:app", "--access-logformat", "''"]