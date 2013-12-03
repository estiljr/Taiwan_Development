--Modified and uploaded to db on 22-11-2013;


CREATE TABLE model_gi.zline_pl
(
  gid serial NOT NULL,
  geom geometry (LINESTRING,3826),
  height real NOT NULL DEFAULT (-9999.0),
  height1 real NOT NULL DEFAULT (-9999.0),
  height2 real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  intrp_ends integer NOT NULL DEFAULT 0,
  lowest_val integer NOT NULL DEFAULT 0,
  comment text,
  CONSTRAINT zline_pl_pkey PRIMARY KEY (gid )
);

CREATE INDEX sidx_zline_pl
  ON model_gi.zline_pl
  USING gist
  (geom );
  
-------------------------------------------------------------------------------------------
CREATE TABLE model_gi.zline_plpt_pl
(
  gid serial NOT NULL,
  geom geometry (LINESTRING,3826),
  height real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  comment text,
  CONSTRAINT zline_plpt_pl_pkey PRIMARY KEY (gid )
);

CREATE INDEX sidx_zline_plpt_pl
  ON model_gi.zline_plpt_pl
  USING gist
  (geom );
  
-------------------------------------------------------------------------------------------  
  CREATE TABLE model_gi.zline_plpt_pt
(
  gid serial NOT NULL,
  geom geometry (LINESTRING,3826),
  height real NOT NULL DEFAULT (-9999.0),
  thick integer NOT NULL DEFAULT 1,
  CONSTRAINT zline_plpt_pt_pkey PRIMARY KEY (gid )
);

CREATE INDEX sidx_zline_plpt_pt
  ON model_gi.zline_plpt_pt
  USING gist
  (geom );

-------------------------------------------------------------------------------------------    
CREATE TABLE model_gi.zarea
(
  gid serial NOT NULL,
  geom geometry (POLYGON,3826),
  height real NOT NULL DEFAULT (-9999.0),
  lowest_val integer NOT NULL DEFAULT 1,
  comment text,
  CONSTRAINT zarea_pkey PRIMARY KEY (gid )
);

CREATE INDEX sidx_zarea
  ON model_gi.zarea
  USING gist
  (geom );

 -------------------------------------------------------------------------------------------    
CREATE TABLE model_gi.narea
(
  gid serial NOT NULL,
  geom geometry (POLYGON, 3826),
  method character varying(50) NOT NULL,
  value real NOT NULL DEFAULT 0.03,
  comment text ,
  CONSTRAINT narea_pkey PRIMARY KEY (gid )
);

CREATE INDEX sidx_narea
  ON model_gi.narea
  USING gist
  (geom );