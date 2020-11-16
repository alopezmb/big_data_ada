#Dockerfile for spark-submit container.

FROM bde2020/spark-submit:2.4.4-hadoop2.7

ARG JAR_NAME=${JAR_NAME}
ENV SPARK_APPLICATION_JAR_LOCATION=/spark-jars/${JAR_NAME}


COPY ./${JAR_NAME} ${SPARK_APPLICATION_JAR_LOCATION}/.
COPY ./wait-for-it.sh /.
COPY ./submit_job.sh /.


RUN chmod +x wait-for-it.sh submit_job.sh

CMD ["/wait-for-it.sh","spark-master:7077","--","/submit_job.sh"]
#CMD ["/test.sh"]
