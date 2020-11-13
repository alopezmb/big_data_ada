#!/bin/bash

export SPARK_MASTER_URL=spark://${SPARK_MASTER_NAME}:${SPARK_MASTER_PORT}
export SPARK_HOME=/spark

/spark/bin/spark-submit \
    --class ${SPARK_APPLICATION_MAIN_CLASS} \
    --master ${SPARK_MASTER_URL} \
    ${SPARK_SUBMIT_ARGS} \
    ${SPARK_APPLICATION_JAR_LOCATION} ${SPARK_APPLICATION_ARGS}
