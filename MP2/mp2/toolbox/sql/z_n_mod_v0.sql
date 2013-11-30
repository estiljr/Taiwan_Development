CREATE TABLE model_gi.zlines_pl
(
  gid serial NOT NULL,
  geom geometry,
  height real NOT NULL DEFAULT (-9999.0),
  height1 real NOT NULL DEFAULT (-9999.0),
  height2 real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  intrp_ends integer NOT NULL DEFAULT 0,
  lowest_val integer NOT NULL DEFAULT 0,
  comment text,
  CONSTRAINT zlines_pl_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'LINESTRING'::text OR geom IS NULL),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 27700)
)

CREATE INDEX sidx_zlines_pl
  ON model_gi.zlines_pl
  USING gist
  (geom );
  
-------------------------------------------------------------------------------------------
CREATE TABLE model_gi.zlines_plpt_pl
(
  gid serial NOT NULL,
  geom geometry,
  height real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  comment text,
  CONSTRAINT zlines_plpt_pl_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'LINESTRING'::text OR geom IS NULL),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 27700)
)

CREATE INDEX sidx_zlines_plpt_pl
  ON model_gi.zlines_plpt_pl
  USING gist
  (geom );
  
-------------------------------------------------------------------------------------------  
  CREATE TABLE model_gi.zlines_plpt_pt
(
  gid serial NOT NULL,
  geom geometry,
  height real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  CONSTRAINT zlines_plpt_pt_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'POINT'::text OR geom IS NULL),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 27700)
)

CREATE INDEX sidx_zlines_plpt_pt
  ON model_gi.zlines_plpt_pt
  USING gist
  (geom );

-------------------------------------------------------------------------------------------    
CREATE TABLE model_gi.zareas
(
  gid serial NOT NULL,
  geom geometry,
  height real NOT NULL DEFAULT (-9999.0),
  lowest_val integer NOT NULL DEFAULT 1,
  comment text,
  CONSTRAINT zareas_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'POLYGON'::text OR geom IS NULL),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 27700)
)

CREATE INDEX sidx_zareas
  ON model_gi.zareas
  USING gist
  (geom );

 -------------------------------------------------------------------------------------------    
CREATE TABLE model_gi.nareas
(
  gid serial NOT NULL,
  geom geometry,
  method character varying(50) NOT NULL,
  value real NOT NULL DEFAULT 0.03,
  comment text ,
  CONSTRAINT nareas_pkey PRIMARY KEY (gid ),
  CONSTRAINT enforce_dims_geom CHECK (st_ndims(geom) = 2),
  CONSTRAINT enforce_geotype_geom CHECK (geometrytype(geom) = 'POLYGON'::text OR geom IS NULL),
  CONSTRAINT enforce_srid_geom CHECK (st_srid(geom) = 27700)
)

CREATE INDEX sidx_nareas
  ON model_gi.nareas
  USING gist
  (geom );