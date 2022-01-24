# Using LTS Ubuntu Focal
FROM docker.io/ubuntu:20.04

ENV ARCH=amd64 \
    PYTHON_VERSION=3.8.12

RUN apt update && \
    apt install -y curl gpg unzip libdigest-sha-perl build-essential zlib1g zlib1g-dev

# B26995E310250568 is the current gpg key ID for python
#RUN curl -OsL "https://keybase.io/ambv/pgp_keys.asc?fingerprint=e3ff2839c048b25c084debe9b26995e310250568" | gpg --import - && \
RUN cd /tmp && \
    curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xB26995E310250568" | gpg --import - && \
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

RUN useradd -m -d /home/app -s /bin/bash app

USER app:app

WORKDIR /home/app

COPY src/ .

RUN python3 -m pip install \
    -r requirements.txt

ENTRYPOINT ["python3",""]