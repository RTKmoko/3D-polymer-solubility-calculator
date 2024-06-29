FROM python:3.8.3-buster

WORKDIR /opt
RUN mkdir -p /opt/venv
# Update python, pip, venv
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install setuptools wheel
ENV PATH=/opt/venv/bin:$PATH

COPY psc_3d psc_3d
COPY *.* .

RUN python3 -m pip install -r requirements.txt && \
  python3 setup.py bdist_wheel && \
  python3 -m pip install dist/*.whl

ENTRYPOINT ["python3", "-m", "psc_3d"]
CMD []