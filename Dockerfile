FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir requests python-telegram-bot pandas numpy ollama

CMD ["python", "main_fixed.py"]
