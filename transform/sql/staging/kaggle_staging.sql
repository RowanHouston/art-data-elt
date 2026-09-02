/*
2 main operations:
1) Rename all columns ensuring consistency across all sources (e.g all artist ids should be called artist_id)
2) Since the final schema has already been decided upon, roughly remove columns that will never be used (borderline ones can be kept) */

CREATE TABLE staging.stg_kaggle_artists AS
SELECT
    "artist_id",
    "full_name" AS artist_name,
    "first_name",
    "middle_names",
    "last_name",
    "nationality",
    "birth" AS birth_year,
    "death" AS death_year
    'kaggle' AS source
FROM raw.kaggle_artist;

CREATE TABLE staging.stg_kaggle_image_link AS
SELECT
    "work_id" AS artwork_id,
    "url" AS object_url,
    "thumbnail_large_url" AS image_url
FROM raw.kaggle_image_link;

CREATE TABLE staging.stg_kaggle_museum AS
SELECT 
    "museum_id",
    "name" as museum_name,
FROM raw.kaggle_museum;

CREATE TABLE staging.stg_kaggle_product_size AS
SELECT
    "work_id" AS artwork_id,
    "size_id"
FROM raw.kaggle_product_size;

CREATE TABLE staging.stg_kaggle_canvas_size AS
SELECT
    "size_id",
    "width" * (2.54) AS width_cm
    "height" * (2.54) AS height_cm
FROM raw.kaggle_canvas_size;

CREATE TABLE staging.stg_kaggle_work AS
SELECT
    "work_id" AS artwork_id,
    "name" AS title,
    "artist_id",
    "museum_id"
FROM raw.kaggle_work;
