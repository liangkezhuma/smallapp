FROM python:3.8-alpine

RUN adduser -D smallapp

WORKDIR /home/smallapp

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY smallapp.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP smallapp.py

RUN chown -R smallapp:smallapp ./
USER smallapp

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
