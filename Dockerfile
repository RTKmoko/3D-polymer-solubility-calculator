FROM ubuntu:latest

WORKDIR /opt

RUN pip install --upgrade pip && \
    pip install numpy matplotlib rich

RUN sudo apt update && \
    sudo apt upgrade -y