FROM ubuntu:latest

WORKDIR /opt

RUN pip install --upgrade-pip && \
    pip install numb

RUN sudo apt update && \
    sudo apt upgrade -y