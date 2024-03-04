-- Table: lusha.contacts_data

-- DROP TABLE IF EXISTS lusha.contacts_data;

CREATE TABLE IF NOT EXISTS lusha.contacts_data
(
    name text COLLATE pg_catalog."default",
    phone_number text COLLATE pg_catalog."default",
    source text COLLATE pg_catalog."default",
    location text COLLATE pg_catalog."default",
    work_email text COLLATE pg_catalog."default",
    parsed_phone_number text COLLATE pg_catalog."default",
    country_code text COLLATE pg_catalog."default",
    parsed_name text COLLATE pg_catalog."default",
    score bigint NOT NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS lusha.contacts_data
    OWNER to postgres;
-- Index: idx_parsed_phone_number

-- DROP INDEX IF EXISTS lusha.idx_parsed_phone_number;

CREATE INDEX IF NOT EXISTS idx_parsed_phone_number
    ON lusha.contacts_data USING btree
    (parsed_phone_number COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;