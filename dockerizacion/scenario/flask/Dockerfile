FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app
COPY ./requirements.txt /app/.

RUN pip3 install -r /app/requirements.txt

