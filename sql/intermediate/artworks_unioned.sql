SELECT
    at.artist_name AS artist_full_name,
    aw.title,
    aw.department,
    aw.classification,
    aw.medium,
    aw.date,
    aw.begin_date,
    aw.end_date,
    aw.credit_line,
    aw.height_cm,
    aw.width_cm,
    aw.depth_cm,
    aw.image_url,
    aw.object_url,
    'MoMA' AS museum,
    aw.source
FROM staging.stg_moma_artworks AS aw LEFT JOIN staging.stg_moma_artists AS at
ON aw.artist_id = at.artist_id

UNION ALL

SELECT
    ma.artist_name AS artist_full_name,
    ma.title,
    ma.department,
    ma.classification,
    ma.medium,
    ma.date,
    ma.begin_date,
    ma.end_date,
    ma.credit_line,
    mm.height_cm,
    mm.width_cm,
    mm.depth_cm,
    ma.image_url,
    ma.object_url,
    'The Met' AS museum,
    ma.source
FROM staging.stg_met_artworks AS ma LEFT JOIN intermediate.int_met_measurements AS mm
ON ma.artwork_id = mm.artwork_id

UNION ALL

SELECT
    ka.artist_name AS artist_full_name,
    kw.title,
    'Paintings' AS department,
    NULL AS classification,
    NULL AS medium,
    NULL AS date,
    NULL AS begin_date,
    NULL AS end_date,
    NULL AS credit_line,
    kcs.height_cm,
    kcs.width_cm,
    NULL AS depth, -- all paintings so depth ~0, just leave as null since paintings in other datasets have depth including frames
    kil.image_url,
    kil.object_url,
    km.museum_name AS museum,
    'Kaggle Famous Paintings Dataset' AS source
FROM
staging.stg_kaggle_artists AS ka 
LEFT JOIN staging.stg_kaggle_work AS kw ON ka.artist_id = kw.artist_id
LEFT JOIN staging.stg_kaggle_product_size AS kps ON kw.artwork_id = kps.artwork_id
LEFT JOIN staging.stg_kaggle_canvas_size AS kcs ON kps.size_id = kcs.size_id
LEFT JOIN staging.stg_kaggle_image_link AS kil ON kw.artwork_id = kil.artwork_id
LEFT JOIN staging.stg_kaggle_museum AS km ON kw.museum_id = km.museum_id;
