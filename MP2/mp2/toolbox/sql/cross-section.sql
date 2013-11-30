
CREATE TABLE bg_gi.river_section
(
	gid serial NOT NULL,
	the_geom geometry,
	river_name character varying(50),
	section_name character varying(50),
	river_section_name character varying(50),
	left_bank_id integer,
	right_bank_id integer,
	bed_id integer,
	lb_easting real,
	lb_northing real,
	lb_z real,
	rb_easting real,
	rb_northing real,
	rb_z real,
	survey_year integer,
	next_section_id integer,
	dist_to_next real,
	no_of_points integer
)

CREATE TABLE bg_gi.section_point
(
  gid serial NOT NULL,
  the_geom geometry,
  river_section_id integer,
 
  x real,
  y real,
  easting real,
  northing real,        
  roughness real,       
  note character varying(50),
  marker character varying(50),
  deactivation character varying(50)
)



