FROM python:3.8.10

WORKDIR /opt

RUN pip install --upgrade pip && \
    pip install scikit-learn

ADD test.py .

CMD ["python","./test.py"]