FROM python:3.8.3-alpine

RUN apk update && \
    apk upgrade && \
    apk add --no-cache openssl bash python3 py3-pip

WORKDIR /opt

ADD requirement.txt .

RUN python -m pip install pip --upgrade \
    && python -m pip install -r requirement.txt


ENTRYPOINT ["python", "-m", "/usr/local/lib/python3.8/site-packages"]
CMD []