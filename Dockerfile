FROM python:3.12-slim
RUN useradd -M testuser
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chown -R testuser:testuser /app
USER testuser
CMD gunicorn library.library.wsgi:application --bind 0.0.0.0:8000 --workers  ${GUNICORN_WORKERS:-3}