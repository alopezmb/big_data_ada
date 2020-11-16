#!/bin/bash

bin/kafka-console-consumer.sh \
    --bootstrap-server kafka:9092 \
    --topic flight_delay_classification_request \
    --from-beginning