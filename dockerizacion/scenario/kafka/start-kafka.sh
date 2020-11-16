#!/bin/bash

create-topics.sh &
unset KAFKA_CREATE_TOPICS

/etc/confluent/docker/run