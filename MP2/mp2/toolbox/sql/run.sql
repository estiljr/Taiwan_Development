CREATE TABLE model_meta.run
(
  id serial NOT NULL,
  name character varying(254) NOT NULL,
  --domain_gid integer NOT NULL DEFAULT 0,
  scenario_id integer NOT NULL,
  dir_run character varying(254),
  
  requires_generation boolean NOT NULL DEFAULT False,
  action character varying(50) NOT NULL DEFAULT 'n',
  lock boolean NOT NULL DEFAULT true,
  simulator_status character varying(50) NOT NULL DEFAULT 'pending',
  autocheck_status character varying(50) NOT NULL DEFAULT 'pending',
  simulation_count integer NOT NULL DEFAULT 0,
  intervention_required boolean NOT NULL DEFAULT true,

  rerun boolean NOT NULL DEFAULT false,
  reset_auto_retry boolean NOT NULL DEFAULT false,
  cancel boolean NOT NULL DEFAULT false,
  
  sys_message text,
  condor_id character varying(16),  
  run_ret integer,
  qa_ret character varying(6),

  modeller character varying(254),
  reviewer character varying(254),
  comments text,

  generation_time timestamp without time zone,
  completion_time timestamp without time zone,

  time_step real NOT NULL,
  
  model_type character varying(50),
  solver_type character varying(50) NOT NULL ,
  
  start_time real NOT NULL,
  finish_time real NOT NULL,

  save_int_2d real NOT NULL,   
  save_int_1d real NOT NULL, 
  
  software character(50),
  simulation_time_hr double precision,

  mb_err_perc double precision,
  priority integer DEFAULT 0,
  
  need_archive BOOLEAN NOT NULL DEFAULT FALSE,
  archive_msg  text,
  
  tag text,
  
  CONSTRAINT run_pkey PRIMARY KEY (id ),
  CONSTRAINT fk1_run FOREIGN KEY (domain_gid)
      REFERENCES model_gi.domain (gid) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk2_run FOREIGN KEY (scenario_id)
      REFERENCES model_meta.scenarios (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT uq_name UNIQUE (name)
);

action:
    n - no
    r -  run no re-gen
    g  - run with generation
    a - advanced run 
    p - postprocess

lock: true, false   
   
simulator_status:
	pending
	start
	packaging
	running
	succeeded
	failed
	
solver_type:
	adi_2d
	tvd_2d

model_type:
















CREATE TABLE model_meta.run
(
  id serial ,
  name character varying(254) ,
  --domain_gid integer  DEFAULT 0,
  scenario_id integer ,
  dir_run character varying(254),
  
  requires_generation boolean  DEFAULT False,
  action character varying(50)  DEFAULT 'n',
  lock boolean  DEFAULT true,
  simulator_status character varying(50)  DEFAULT 'pending',
  autocheck_status character varying(50)  DEFAULT 'pending',
  simulation_count integer  DEFAULT 0,
  intervention_required boolean  DEFAULT true,

  rerun boolean  DEFAULT false,
  reset_auto_retry boolean  DEFAULT false,
  cancel boolean  DEFAULT false,
  
  sys_message text,
  condor_id character varying(16),  
  run_ret integer,
  qa_ret character varying(6),

  modeller character varying(254),
  reviewer character varying(254),
  comments text,

  generation_time timestamp without time zone,
  completion_time timestamp without time zone,

  time_step real ,
  
  model_type character varying(50),
  solver_type character varying(50)  ,
  
  start_time real ,
  finish_time real ,

  save_int_2d real ,   
  save_int_1d real , 
  
  software character(50),
  simulation_time_hr double precision,

  mb_err_perc double precision,
  priority integer DEFAULT 0,
  
  need_archive BOOLEAN  DEFAULT FALSE,
  archive_msg  text,
  
  tag text,
  
  CONSTRAINT run_pkey PRIMARY KEY (id ),
  CONSTRAINT fk2_run FOREIGN KEY (scenario_id)
      REFERENCES model_meta.scenarios (id) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT uq_name UNIQUE (name)
);