FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY ./src .

CMD wait-for-it -s "${REDIS_HOST}:${REDIS_PORT}" -s "${DB_HOST}:${DB_PORT}" --timeout 120 && gunicorn wsgi_app:app --bind=0.0.0.0:8000
