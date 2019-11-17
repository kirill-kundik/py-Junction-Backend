FROM python:3.7.3

ADD . /junction-server
WORKDIR /junction-server

RUN pip3 install -e .

ARG APP_PORT
EXPOSE $APP_PORT

CMD alembic upgrade head && gunicorn -w 8 -b 0.0.0.0:$APP_PORT "main:application"
