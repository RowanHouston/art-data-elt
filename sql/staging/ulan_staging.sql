-- Note that the ulan python script effectively handles the naming of 
-- all the ulan data, so this file is mostly for the pipeline and possible changes.

CREATE TABLE staging.stg_ulan_info AS
SELECT * FROM raw.ulan_info;

CREATE TABLE staging.stg_ulan_names AS
SELECT * FROM raw.ulan_names;
