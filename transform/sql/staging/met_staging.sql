/*
2 main operations:
1) Rename all columns ensuring consistency across all sources (e.g all artist ids should be called artist_id)
2) Since the final schema has already been decided upon, roughly remove columns that will never be used (borderline ones can be kept) */

CREATE TABLE staging.met_objects AS
SELECT 
    "object_id" as artwork_id,
    "primaryImage" AS image_url,
    "title" AS title,
    "artistDisplayName" AS artist_name,
    "artistNationality" AS nationality,
    "artistBeginDate" AS birth_year,
    "artistEndDate" AS death_year,
    "artistGender" AS gender,
    "artistULAN_URL" AS ulan_url,
    "objectEndDate" AS date,
    "dimensions" AS dimensions_string,
    "dimensionsParsed" AS dimensions_json,
    "creditLine" AS credit_line,
    "objectURL" as url
FROM raw.met_objects;