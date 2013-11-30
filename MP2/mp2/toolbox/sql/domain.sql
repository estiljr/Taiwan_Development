--Modified and uploaded to db on 22-11-2013;

CREATE TABLE model_gi.domain
(
  gid serial NOT NULL,
  geom geometry(POLYGON, 3826),
  name character varying(254) NOT NULL,
  domain_ws character varying(254),
  cell_size real NOT NULL,
  us_domain_gids integer[],
  ds_domain_gids integer[],
  us_bdy_gids integer[],
  ds_bdy_gids integer[],
  ds_end boolean,
  
  --date_gen timestamp without time zone,
  --date_mod timestamp without time zone,
  
  modeller character varying(254) NOT NULL,
  reviewer character varying(254) NOT NULL,  
  log text,
  comment text,
  status character varying(254) NOT NULL,
  
  CONSTRAINT domain_pkey PRIMARY KEY (gid )
  );
  

CREATE INDEX idx_domain_name
  ON model_gi.domain
  USING btree
  (name );

CREATE INDEX sidx_domain
  ON model_gi.domain
  USING gist
  (geom );



