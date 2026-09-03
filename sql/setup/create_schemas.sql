CREATE SCHEMA IF NOT EXISTS raw IS
'Raw data loaded from python scripts';

CREATE SCHEMA IF NOT EXISTS staging IS
'Reduced tables from raw with renamed and retyped columns';

CREATE SCHEMA IF NOT EXISTS intermediate IS
'Cross-source joins, unions, and entity resolutions';

CREATE SCHEMA IF NOT EXISTS final IS
'Final schema with foreign and primary keys';