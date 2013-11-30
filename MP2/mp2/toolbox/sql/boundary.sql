--Modified and uploaded to db on 22-11-2013;

CREATE TABLE model_gi.boundary
(
  gid serial NOT NULL,
  geom geometry (LINESTRING,3826),
  type character varying(254) NOT NULL,
  value real,
  domain_gid integer,
  flow_point_gid integer,
  CONSTRAINT boundary_pkey PRIMARY KEY (gid ),
  CONSTRAINT fk_boundary FOREIGN KEY (domain_gid)
      REFERENCES model_gi.domain (gid) MATCH SIMPLE
      ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX sidx_boundary
  ON model_gi.boundary
  USING gist
  (geom );