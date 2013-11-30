
ALTER TABLE [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column TO new_column
	
CREATE TABLE bg_gi.rain_gauge
(
	gid serial NOT NULL,
	geom geometry,
	
	gauge_name character varying(50),
	wra_gauge character varying(50),
	cwb_gauge character varying(50),
	
	basin character varying(50),
	river character varying(50),
	county character varying(50),	
	
	minutely_yrs character varying(250),
	hourly_yrs character varying(250),	
	daily_yrs character varying(250),
	monthly_yrs character varying(250),		
		
	minutely_no_yrs integer,
	hourly_no_yrs integer,
	daily_no_yrs integer,
	monthly_no_yrs integer,
	
	has_data boolean NOT NULL default false,
	used boolean NOT NULL default false,
	comment text,
	
	CONSTRAINT rain_gauge_pk PRIMARY KEY (gid)
)

CREATE TABLE bg_gi.flow_gauge
(
	gid serial NOT NULL,
	geom geometry(Point, 4326),
	
	gauge_name character varying(50),
	wra_gauge character varying(50),

	elevation real,
	basin character varying(50),
	river character varying(50),
	county character varying(50),	
	
	years character varying(250),		
	no_yrs integer,
		
	has_data boolean NOT NULL default false,
	used boolean NOT NULL default false,
	
	comment text,
	
	CONSTRAINT flow_gauge_pk PRIMARY KEY (gid)
)


ALTER TABLE bg_gi.flow_gauge ADD CONSTRAINT flow_gauge_pk PRIMARY KEY (gid)
ALTER TABLE bg_gi.rain_gauge ADD CONSTRAINT rain_gauge_pk PRIMARY KEY (gid)