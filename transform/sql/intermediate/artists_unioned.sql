SELECT
    artist_name,
    nationality,
    gender,
    birth_year,
    death_year,
    ulan_id,
    'https://www.wikidata.org/wiki/' || "Wikidata_id" AS artist_wikidata_url,
    source
FROM staging.stg_moma_artists

UNION all

SELECT 
    artist_name,
    nationality,
    gender,
    birth_year,
    death_year,
    string_to_text("artistULAN_URL", '/')[6] AS ulan_id,
    artist_wikidata_url,
    source
FROM staging.stg_met_objects

UNION ALL

SELECT 
    artist_name,
    first_name, --might be removed later (obtained for met/moma via getty??)
    last_name,
    nationality,
    gender,
    birth_year,
    death_year,
    source
FROM staging.stg_kaggle_artists;