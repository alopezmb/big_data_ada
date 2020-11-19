# Setup Kafka
import json
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],api_version=(2,3,0))
PREDICTION_TOPIC = 'flight_delay_classification_request'
producer.send(PREDICTION_TOPIC, b'test message')

