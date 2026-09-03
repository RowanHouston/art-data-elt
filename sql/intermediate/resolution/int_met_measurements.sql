/* Main idea is just to extract all possible measurements even though we're 
really only going to use a few of them.
Note that in 3 dimensions (i.e reality) we really only have 2 non-height dimensions,
so when we have diameter we know it points to a somehow circular object.
Although this probably wont be used in the final schema
*/
CREATE TABLE intermediate.int_met_measurements AS
WITH measurements_unnested AS (
    SELECT
        artwork_id,
        jsonb_array_elements(measurements::jsonb) AS elem
    FROM staging.stg_met_artworks
    WHERE measurements IS NOT NULL
),
measurements_extracted AS (
    SELECT
        artwork_id,
        elem->>'elementName' AS element_name,
        (elem->'elementMeasurements'->>'Height')::numeric AS height_cm,
        (elem->'elementMeasurements'->>'Width')::numeric AS width_cm,
        (elem->'elementMeasurements'->>'Depth')::numeric AS depth_cm,
        
        COALESCE(
            (elem->'elementMeasurements'->>'Diameter')::numeric,
            CASE WHEN elem->>'elementName' = 'Diameter' 
                THEN (elem->'elementMeasurements'->>'Diameter')::numeric 
            END
        ) AS diameter_cm,

        CASE elem->>'elementName' -- this is roughly bsed on the # of occurences in the data
            WHEN 'Overall' THEN 1
            WHEN 'Sheet' THEN 2
            WHEN 'Image' THEN 3
            WHEN 'Plate' THEN 4
            WHEN 'Framed' THEN 5
            WHEN 'Unframed' THEN 6
            WHEN 'Overall with mounting' THEN 7
            WHEN 'Mat' THEN 8
            WHEN 'Other' THEN 9
            ELSE 10
        END AS priority
    FROM measurements_unnested

    WHERE elem->>'elementName' NOT IN (
        'Length at CB', 'Length at CF', 'Length at Side Seam',
        'Heel to Toe', 'Center Front', 'Center Back',
        'Tenon/Tang', 'Sounding Length', 'Cord'
    ) -- these are only clothing (?) related so we don't need them
)
SELECT DISTINCT ON (artwork_id)
    artwork_id,
    height_cm,
    width_cm,
    depth_cm,
    diameter_cm
FROM measurements_extracted
ORDER BY artwork_id, priority;