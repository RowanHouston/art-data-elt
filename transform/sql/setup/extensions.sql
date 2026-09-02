CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_ulan_names_trgm ON staging.stg_ulan_names 
USING gin(name gin_trgm_ops);
