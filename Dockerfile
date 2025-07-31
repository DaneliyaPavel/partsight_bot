FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    AIOGRAM_NO_UVLOOP=1 \
    PYTHONPATH=/app

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "bot.main"]
