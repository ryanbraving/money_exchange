# # syntax=docker/dockerfile:1
# FROM python:3.9
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/

FROM python:3.13-alpine
ENV PYTHONUNBUFFERED=1
# Set work directory
WORKDIR /code
# Install build dependencies for psycopg
RUN apk add --no-cache gcc musl-dev libpq-dev
# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libpq-dev netcat-openbsd
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

CMD ["gunicorn", "money_exchange.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "60"]
