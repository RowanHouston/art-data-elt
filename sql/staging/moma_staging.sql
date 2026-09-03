/*
2 main operations:
1) Rename all columns ensuring consistency across all sources (e.g all artist ids should be called artist_id)
2) Since the final schema has already been decided upon, roughly remove columns that will never be used (borderline ones can be kept) */
CREATE TABLE staging.stg_moma_artists AS
SELECT
	"ConstituentID" AS artist_id,
	"DisplayName" AS artist_name,
	"Nationality" AS nationality,
	"Gender" AS gender,
	"BeginDate" AS birth_year,
	"EndDate" AS death_year,
	"ULAN" AS ulan_id,
	"Wiki QID" AS wikidata_id
	'moma' AS source
FROM raw.moma_artists;

CREATE TABLE staging.stg_moma_artworks AS
SELECT
    "ObjectID" AS artwork_id,
	"ConstituentID" AS artist_id,
	"Title" AS title,
	"Date" AS date,
	"BeginDate" AS begin_date,
	"EndDate" AS end_date
	"Classificatoin" AS classification,
	"Department" AS department,
	"Medium" AS medium
    "CreditLine" AS credit_line,
	"URL" AS object_url,
	"ImageURL" AS image_url,
    "Depth" AS depth_cm,
    "Height" AS height_cm,
    "Width" AS width_cm,
from raw.moma_artworks;