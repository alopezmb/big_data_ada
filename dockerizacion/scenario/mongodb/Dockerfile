FROM mongo:4.4.1

COPY data /usr/src/flight_prediction/.
# the /docker-entrypoint-initdb.d/ path to deploy custom .js or .sh setup scripts
COPY import_distances.sh /docker-entrypoint-initdb.d/
