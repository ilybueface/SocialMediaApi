FROM python:3.12-slim
WORKDIR /app
COPY requirements-tg.txt .
RUN pip install -r requirements-tg.txt
COPY . .
CMD ["python", "telegram_bot/bot.py"]