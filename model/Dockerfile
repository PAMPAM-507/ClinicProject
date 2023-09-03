FROM python:3.8
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /model

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install scipy requests djangorestframework-simplejwt
RUN pip install --upgrade pip
COPY ./APIForModel ./APIForModel

EXPOSE 8001








