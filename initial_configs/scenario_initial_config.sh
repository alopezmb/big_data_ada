#!/bin/bash

echo 'Copying trained models to the scenario...'


sudo cp -r pyspark/models ../scenario/spark/models
sudo chown -R ${USER}:${USER} ../scenario/spark/models/

echo "Models copied! Now let's place the resulting JAR in the scenario directory..."

read -p 'Please specify ONLY the NAME of the resulting JAR (without .jar): ' jarname

sudo cp $(sudo find ./jar_builder/scala_projects/flight_prediction_cassandra/target -name "*.jar") \
../scenario/spark/${jarname}.jar

sudo sudo chown ${USER}:${USER} ../scenario/spark/${jarname}.jar

echo "JAR file ${jarname}.jar copied! The initial configuration process has finished."