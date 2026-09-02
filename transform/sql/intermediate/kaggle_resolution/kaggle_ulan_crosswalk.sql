/*
The goal is to obtain that doesn't exist in some of the sources (e.g: gender for the kaggle set)
via the getty union list of artist names lookup table.
(i.e this resolves kaggle artist names into ulan ids)

I briefly considered more robust methods like splink (machine learning comparison approach),
but this seemed far too complex for this scale (especially most information is coming from 
the MET dataset, which is already fairly dense).
*/

--This query gets every name that matches exactly
CREATE TABLE intermediate.kaggle_ulan_crosswalk_rough AS
SELECT
    ka.artist_id AS kaggle_artist_id,
    ul.ulan_id,
    un.name AS matched_name,
    un.is_preferred,
    'exact' AS match_type,
    1.0 AS similarity_score
FROM staging.stg_kaggle_artists ka
JOIN staging.stg_ulan_names un 
    ON LOWER(TRIM(ka.artist_name)) = LOWER(TRIM(un.name))
JOIN staging.stg_ulan_info ul 
    ON un.ulan_id = ul.ulan_id
WHERE -- we want at least one date to match since matching just by name isn't enough
(ka.birth_year = ul.birth_year AND ka.death_year = ul.death_year)
OR (ka.birth_year = ul.birth_year AND ka.death_year IS NULL)
OR (ka.death_year = ul.death_year AND ka.birth_year IS NULL);


--This query break down each name into trigrams and compare similarity.
INSERT INTO intermediate.kaggle_ulan_crosswalk_rough
SELECT
    ka.artist_id AS kaggle_artist_id,
    ul.ulan_id,
    un.name AS matched_name,
    un.is_preferred,
    'fuzzy' AS match_type,
    similarity(LOWER(TRIM(ka.artist_name)), LOWER(TRIM(un.name))) AS similarity_score
FROM staging.stg_kaggle_artists ka
JOIN staging.stg_ulan_names un 
    ON similarity(LOWER(TRIM(ka.artist_name)), LOWER(TRIM(un.name))) > 0.6
JOIN staging.stg_ulan_info ul 
    ON un.ulan_id = ul.ulan_id
WHERE ka.artist_id NOT IN (SELECT kaggle_artist_id FROM intermediate.kaggle_ulan_crosswalk_rough)
AND ((ka.birth_year = ul.birth_year AND ka.death_year = ul.death_year)
OR (ka.birth_year = ul.birth_year AND ka.death_year IS NULL)
OR (ka.death_year = ul.death_year AND ka.birth_year IS NULL));

--This ensures that we don't match multiple names based on similarity score (i.e takes highest)
CREATE TABLE intermediate.kaggle_ulan_crosswalk AS
SELECT DISTINCT ON (kaggle_artist_id)
    kaggle_artist_id,
    ulan_id,
    matched_name,
    match_type,
    similarity_score
FROM intermediate.kaggle_ulan_crosswalk_rough
ORDER BY 
    kaggle_artist_id,
    CASE match_type WHEN 'exact' THEN 1 WHEN 'fuzzy' THEN 2 END,
    similarity_score DESC,
    is_preferred DESC;
