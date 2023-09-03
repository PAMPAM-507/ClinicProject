FROM python:3.8
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /webapp

COPY ./ClinicProject ./ClinicProject

# данный каталоги уже существует в данном проекте
#RUN mkdir /webapp/webauth/static
#RUN mkdir /webapp/webauth/media

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install requests
RUN pip install --upgrade pip
RUN pip install wheel
RUN apt-get install uwsgi -y
RUN pip install gunicorn



#CMD ["python3", "./webauth/manage.py", "runserver", "0.0.0.0:8000"]