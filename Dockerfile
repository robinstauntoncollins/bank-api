FROM python:3.7-alpine

RUN adduser -D bankapi

WORKDIR /home/bankapi

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY bank_api bank_api
COPY migrations migrations
COPY bankapi.py app.db config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R bankapi:bankapi ./
USER bankapi

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]