FROM python:3.10

ENV PYTHONPATH=/

WORKDIR /tests

COPY functional/requirements.txt functional/requirements.txt

RUN pip install --upgrade pip && pip install -r /tests/functional/requirements.txt

COPY . .

CMD wait-for-it -s "${API_HOST}:${API_PORT}" --timeout 60 && pytest -s /tests/functional/src
