FROM python:3.8.3-buster

WORKDIR /opt
RUN mkdir -p /opt/venv

ADD requirement.txt .
# Update python, pip, venv
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate
ENV PATH=/opt/venv/bin:$PATH

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirement.txt

ENTRYPOINT ["python3", "-m", "psc_3d"]
CMD []