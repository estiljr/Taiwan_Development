CREATE TABLE model_meta.run_archive
(
  id serial NOT NULL,
  name character varying(254) NOT NULL,
  version INTEGER not null,
  file_name text NOT NULL,
  comment text,
  archive_time timestamp without time zone,
  
  CONSTRAINT run_archive_pkey PRIMARY KEY (id),
  CONSTRAINT uq_name_version UNIQUE (name,version)
);