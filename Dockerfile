# pull official base image
FROM python:3.9
# set work directory
RUN python -m pip install --upgrade pip
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
# install dependencies
COPY  requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . /code/