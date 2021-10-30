FROM python:3.9.7-slim-buster

ADD ./requirements.txt .
ADD ./src/* .

RUN pip install -r requirements.txt

CMD ["python", "__init__.py"]
