--Modified and uploaded to db on 22-11-2013;

CREATE TABLE model_meta.scenarios
(
  id serial NOT NULL,
  description character varying(254) NOT NULL,
  suffix character varying(254) NOT NULL,
  rp integer NOT NULL,
  defended boolean NOT NULL,
  CONSTRAINT scenarios_pkey PRIMARY KEY (id )
);

CREATE UNIQUE INDEX scenario_id
  ON model_meta.scenarios
  USING btree
  (id )
  WITH (FILLFACTOR=100);