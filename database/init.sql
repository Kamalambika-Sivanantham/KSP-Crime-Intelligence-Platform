-- Run automatically by the postgres container on first init (mounted to docker-entrypoint-initdb.d)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- fuzzy text search for suspect/name lookups
