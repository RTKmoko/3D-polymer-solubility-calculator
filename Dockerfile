FROM ubuntu:latest

WORKDIR /opt

RUN pip install --upgrade-pip -y
    pip install numb