FROM mongo:4.4.1

# environment variables
ENV MONGO_INITDB_ROOT_USERNAME=root
ENV MONGO_INITDB_ROOT_PASSWORD=password

# When a container is started for the first time it will execute files with extensions .sh and .js that are found in
# /docker-entrypoint-initdb.d
COPY import_distances.sh /docker-entrypoint-initdb.d
COPY data /usr/src/mongodb

# /data/db inside the container, where MongoDB by default will write its data files
# Define mountable directories.
VOLUME ["/data/db"]
