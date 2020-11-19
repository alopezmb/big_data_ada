FROM hseeberger/scala-sbt:8u242_1.3.10_2.12.10

WORKDIR ./

COPY ./buildjar.sh ./

RUN chmod +x buildjar.sh

CMD ["bash","./buildjar.sh"]