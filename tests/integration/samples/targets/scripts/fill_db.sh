#!/bin/bash
set -e

#https://gis.stackexchange.com/a/13974

# Creating tables
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION postgis;
    CREATE TABLE targets (
        id INTEGER PRIMARY KEY,
        ra DOUBLE PRECISION,
        dec DOUBLE PRECISION,
        sr DOUBLE PRECISION
    );
    CREATE TABLE match (
        id SERIAL,
        target INTEGER REFERENCES targets(id),
        object_id VARCHAR(20),
        candid VARCHAR(200),
        date TIMESTAMP
    );
    COPY targets (id, ra, dec, sr) FROM '/data/targets.csv' DELIMITER ',' CSV;

    CREATE FUNCTION degrees_to_meters(degrees DOUBLE PRECISION)
    RETURNS DOUBLE PRECISION
    LANGUAGE plpgsql
    AS '
    DECLARE
       EARTH_RADIUS_METERS constant numeric := 6371008.77141506;
       meters DOUBLE PRECISION;
    begin
      SELECT (2 * PI() * EARTH_RADIUS_METERS * degrees) / 360 INTO meters;
      RETURN meters;
    end;
    ';

    CREATE FUNCTION meters_to_degrees(meters DOUBLE PRECISION)
    RETURNS DOUBLE PRECISION
    LANGUAGE plpgsql
    AS
    '
    DECLARE
       EARTH_RADIUS_METERS constant numeric := 6371008.77141506;
       degrees DOUBLE PRECISION;
    begin
      SELECT (meters * 360) / (2* PI() * EARTH_RADIUS_METERS) INTO degrees;
      RETURN degrees;
    end;
    ';
EOSQL
