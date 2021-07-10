FROM python:3.6-slim

COPY ./Pipfile ./Pipfile.lock /

RUN pip install --upgrade pip && pip install pipenv
RUN pipenv install --system --dev

WORKDIR /app
COPY . /app

CMD python run.py
