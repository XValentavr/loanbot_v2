FROM python:3.8

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY src/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
