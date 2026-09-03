SELECT
    ma.artist_name,
    ma.nationality,
    ma.gender,
    TRIM(split_part(un.name, ', ', 1)) AS last_name,
    TRIM(split_part(un.name, ', ', 2)) AS first_name,
    ma.birth_year,
    ma.death_year,
    ma.ulan_id,
    'https://www.wikidata.org/wiki/' || wikidata_id AS artist_wikidata_url,
    ma.source
FROM staging.stg_moma_artists ma LEFT JOIN staging.stg_ulan_names un
ON ma.ulan_id = un.ulan_id AND un.is_preferred IS TRUE

UNION all

SELECT 
    mo.artist_name,
    mo.nationality,
    mo.gender,
    TRIM(split_part(un.name, ', ', 1)) AS last_name,
    TRIM(split_part(un.name, ', ', 2)) AS first_name,
    mo.birth_year,
    mo.death_year,
    split_part(mo.ulan_url, '/', 6) AS ulan_id,
    mo.artist_wikidata_url,
    mo.source
FROM 
staging.stg_met_objects mo LEFT JOIN staging.stg_ulan_names un
ON split_part(mo.ulan_url, '/', 6) = un.ulan_id AND un.is_preferred IS TRUE

UNION ALL

SELECT 
    artist_name,
    nationality,
    ui.gender,
    first_name,
    last_name,
    birth_year,
    death_year,
    cw.ulan_id,
    NULL AS artist_wikidata_url,
    source
FROM 
staging.stg_kaggle_artists ka 
LEFT JOIN intermediate.kaggle_ulan_crosswalk cw
    ON ka.artist_id = cw.kaggle_artist_id
LEFT JOIN staging.stg_ulan_info ui
    ON cw.ulan_id = ui.ulan_id;