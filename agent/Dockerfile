FROM lucas42/lucos_navbar:2.1.1 AS navbar
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./
COPY --from=navbar lucos_navbar.js ./static/

ENV PYTHONUNBUFFERED=1

CMD gunicorn --bind 0.0.0.0:${PORT} app:app
