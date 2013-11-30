--Modified and uploaded to db on 22-11-2013;

CREATE TABLE model_meta.modeller_log
(
  gid serial NOT NULL,
  geom geometry (POLYGON,3826),
  comment text,
  modeller character varying(254),
  status text,

  CONSTRAINT pk_modeller_log PRIMARY KEY (gid )
);