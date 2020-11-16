FROM confluentinc/cp-kafka:5.3.0

COPY  ./create-topics.sh .
COPY ./start-kafka.sh .

RUN chmod +x create-topics.sh start-kafka.sh

CMD ["./start-kafka.sh"]