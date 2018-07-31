FROM python:latest

RUN pip install geolocation-python pandas

WORKDIR app
