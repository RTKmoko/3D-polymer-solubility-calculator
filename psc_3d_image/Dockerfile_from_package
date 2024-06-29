FROM python:3.8.3-buster

WORKDIR /opt
RUN mkdir -p /opt/venv
# Update python, pip, venv
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    python3 -m pip install --upgrade pip
ENV PATH=/opt/venv/bin:$PATH

ADD requirement.txt .

RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install -r requirement.txt

ENTRYPOINT ["python3", "-m", "psc_3d"]
CMD []