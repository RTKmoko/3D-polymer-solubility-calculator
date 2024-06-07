FROM python:3.8.10

ADD test.py

RUN pip install --upgrade pip

RUN pip install scikit-learn

CMD ["python","./test.py"]