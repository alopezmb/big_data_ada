CREATE KEYSPACE IF NOT EXISTS agile_data_science WITH REPLICATION = {'class':'SimpleStrategy','replication_factor':2};

CREATE TABLE IF NOT EXISTS agile_data_science.origin_dest_distances (
  Origin text,
  Dest text,
  Distance double,
  PRIMARY KEY ((Origin,Dest))
);

COPY agile_data_science.origin_dest_distances FROM '/config_db/origin_dest_distances.csv' WITH HEADER=true;

CREATE TABLE IF NOT EXISTS agile_data_science.flight_delay_classification_response (
  "Origin" text,
  "DayOfWeek" tinyint,
  "DayOfYear" smallint,
  "DayOfMonth" tinyint,
  "Dest" text,
  "DepDelay" smallint,
  "SearchTimestamp" timestamp,
  "FlightDate" timestamp,
  "Carrier" text,
  "Identifier" text,
  "Distance" double,
  "Route" text,
  "Prediction" tinyint,
  PRIMARY KEY ("Identifier")
);
