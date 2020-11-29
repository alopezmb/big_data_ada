FROM tiangolo/meinheld-gunicorn-flask:python3.7
#FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./requirements.txt /app/.
COPY ./wait-for-it.sh /.

RUN pip3 install -r /app/requirements.txt

RUN chmod +x /wait-for-it.sh

CMD ["/wait-for-it.sh","cassandra-1:9042","-t","75","--","/start.sh"]

