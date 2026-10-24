FROM python:3.12-slim
RUN groupadd -g 1000 appuser && useradd -M -u 1000 -g appuser appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chown -R appuser:appuser /app
USER appuser
CMD gunicorn library.library.wsgi:application --bind 0.0.0.0:8000 --workers  ${GUNICORN_WORKERS:-3}