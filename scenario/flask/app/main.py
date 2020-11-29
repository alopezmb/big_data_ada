import sys, os, re
from flask import Flask, render_template, request
from bson import json_util
from cassandra.cluster import Cluster


# Configuration details
import config

# Helpers for search and prediction APIs
import predict_utils

# Set up Flask, Cassandra and Elasticsearch
app = Flask(__name__)

# mongodb://mongodbHostName:27017
#CONNECTION_URI = "mongodb://mongodb:27017"
#client = MongoClient(CONNECTION_URI, connect=False)

#Cassandra
cluster = Cluster(['cassandra-1', 'cassandra-2'], port=9042)
session = cluster.connect('agile_data_science')

import json

# Date/time stuff
import iso8601
import datetime

# Setup Kafka
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['kafka:9092'],api_version=(2,3,0))
PREDICTION_TOPIC = 'flight_delay_classification_request'

import uuid

# Make our API a post, so a search engine wouldn't hit it
@app.route("/flights/delays/predict/classify_realtime", methods=['POST'])
def classify_flight_delays_realtime():
  """POST API for classifying flight delays"""
  
  # Define the form fields to process
  api_field_type_map = \
    {
      "DepDelay": float,
      "Carrier": str,
      "FlightDate": str,
      "Dest": str,
      "FlightNum": str,
      "Origin": str
    }

  # Fetch the values for each field from the form object
  api_form_values = {}
  for api_field_name, api_field_type in api_field_type_map.items():
    api_form_values[api_field_name] = request.form.get(api_field_name, type=api_field_type)
  
  # Set the direct values, which excludes Date
  prediction_features = {}
  for key, value in api_form_values.items():
    prediction_features[key] = value
  
  # Set the derived values
  prediction_features['Distance'] = predict_utils.get_flight_distance(
    session, api_form_values['Origin'],
    api_form_values['Dest']
  )
  #print('Distance:')
  #print(prediction_features['Distance'])

  # Turn the date into DayOfYear, DayOfMonth, DayOfWeek
  date_features_dict = predict_utils.get_regression_date_args(
    api_form_values['FlightDate']
  )
  for api_field_name, api_field_value in date_features_dict.items():
    prediction_features[api_field_name] = api_field_value

  # Add a timestamp
  prediction_features['Timestamp'] = predict_utils.get_current_timestamp()

  # Create a unique ID for this message
  unique_id = str(uuid.uuid4())
  prediction_features['UUID'] = unique_id

  message_bytes = json.dumps(prediction_features).encode()
  producer.send(PREDICTION_TOPIC, message_bytes)
  #producer.flush()

  response = {"status": "OK", "id": unique_id}
  return json_util.dumps(response)

@app.route("/flights/delays/predict_kafka")
def flight_delays_page_kafka():
  """Serves flight delay prediction page with polling form"""
  
  form_config = [
    {'field': 'DepDelay', 'label': 'Departure Delay', 'value': 5},
    {'field': 'Carrier', 'value': 'AA'},
    {'field': 'FlightDate', 'label': 'Date', 'value': '2016-12-25'},
    {'field': 'Origin', 'value': 'ATL'},
    {'field': 'Dest', 'label': 'Destination', 'value': 'SFO'}
  ]
  #distance = predict_utils.get_flight_distance(session, form_config[3]['value'],form_config[4]['value'])
  # <p>Distance: {{distance}}</p>
  return render_template('flight_delays_predict_kafka.html', form_config=form_config)

@app.route("/flights/delays/predict/classify_realtime/response/<unique_id>")
def classify_flight_delays_realtime_response(unique_id):
  """Serves predictions to polling requestors"""

  prediction = predict_utils.get_prediction(session,unique_id)
  response = {"status": "WAIT", "id": unique_id}

  if prediction:
    response["status"] = "OK"
    response["prediction"] = prediction
  
  return json_util.dumps(response)

