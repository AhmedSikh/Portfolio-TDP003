FROM python:latest

ENV APP_HOME /app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN pip install flask

ADD . $APP_HOME/
ENV FLASK_APP=main.py
CMD flask run -h 0 -p 3000