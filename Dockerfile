FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn library.library.wsgi:application --bind 0.0.0.0:8000 --workers  ${GUNICORN_WORKERS:-3}