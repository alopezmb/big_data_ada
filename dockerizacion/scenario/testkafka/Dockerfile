#Install python 3.7 for this container
FROM bitnami/java:1.8

RUN apt-get update && apt-get install -y --no-install-recommends python3.7 python3-pip

COPY ./start.sh .
COPY ./kafka /kafka/.
COPY ./pipeline /kafka/.

COPY ./requirements.txt .
# Install required python packages
RUN pip3 install -r requirements.txt

RUN chmod +x start.sh /kafka/testkafka.sh

CMD ["./start.sh"]

