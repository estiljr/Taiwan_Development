--Modified and uploaded to db on 22-11-2013;

CREATE TABLE condor.client
(
  id serial NOT NULL,
  name text,
  version text,
  os text,
  arch text,
  slots integer,
  run_count integer,
  location text,
  owner text,
  CONSTRAINT pk_client PRIMARY KEY (id ),
  CONSTRAINT uq_client_name UNIQUE (name)
);
--------------------------------------------------------------------------------------------
CREATE TABLE condor.slot
(
  id serial NOT NULL,
  name text,
  machine text,
  state text,
  loadav real,
  memory_g real,
  disk_g real,
  mips real,
  kflops real,
  CONSTRAINT pk_slot PRIMARY KEY (id ),
  CONSTRAINT uq_slot_name UNIQUE (name)
);
--------------------------------------------------------------------------------------------

CREATE TABLE condor.simulation
(
  id serial NOT NULL,
  run_name text,
  --status_within_db text,
  condor_id text,
  host text,
  time_queue timestamp without time zone,
  time_start timestamp without time zone,
  time_update timestamp without time zone,
  run_time time without time zone,
  model_path text,
  current_model_time real,
  run_rate real,
  mb_last_modified timestamp without time zone,
  priority integer,
  size_g real,
  condor_status text,
  cancel boolean NOT NULL DEFAULT false,
  CONSTRAINT key PRIMARY KEY (id )
  --CONSTRAINT fk_run_name FOREIGN KEY (run_name)
   --   REFERENCES model_meta.runs (name) MATCH SIMPLE
   --   ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX idx_run_name
  ON condor.simulation
  USING btree
  (run_name);

CREATE INDEX simulation_condor_id
  ON condor.simulation
  USING btree
  (condor_id);

  --------------------------------------------------------------------------------------------