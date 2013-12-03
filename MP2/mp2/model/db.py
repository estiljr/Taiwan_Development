from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, DateTime , Boolean,MetaData ,VARCHAR

from condor.condor import Slot,Client,JobStatus, CondorSystem
from mp2.model.run import Run, RunArchive
from mp2.model.scenario import Scenario


engine = create_engine('postgresql://taiwan_user:taiwan@UKSD2F0W3J:5432/taiwan', echo=True)  
metadata = MetaData()

''' =============================  start of condor        =========================================== ''' 
slot_table = Table('slot', metadata,
                Column('id', Integer, primary_key=True),
                Column('name',String),
                Column('machine',String),
                Column('state',String),
                Column('loadav',Float),
                Column('memory_g',Float),
                Column('disk_g',Float),                 
                Column('mips',Float),
                Column('kflops',Float),          
                schema='condor')

mapper(Slot, slot_table,  
                    properties={ 'id':  slot_table.c.id,
                                 'name':  slot_table.c.name,
                                 'machine':  slot_table.c.machine,
                                 'state': slot_table.c.state,
                                 'loadav':slot_table.c.loadav,
                                 'memory': slot_table.c.memory_g,
                                 'disk': slot_table.c.disk_g,
                                 'mips':slot_table.c.mips,
                                 'kflops':slot_table.c.kflops,                                       
                                })   

client_table = Table('client', metadata,
                Column('id', Integer, primary_key=True),
                Column('name',String),
                Column('version',String),
                Column('arch',String),
                Column('os',String),                 
                Column('slots',Integer),
                Column('run_count',Integer),                                  
                schema='condor')

mapper(Client, client_table,  
                    properties={ 'id':  client_table.c.id,
                                 'name':  client_table.c.name,
                                 'version': client_table.c.version,
                                 'arch':client_table.c.arch,
                                 'os': client_table.c.os,
                                 'slots': client_table.c.slots,
                                 'run_count':client_table.c.run_count                                  
                                })      

simulation_table = Table('simulation', metadata,
                Column('id', Integer, primary_key=True),
                Column('run_name',String),                
                Column('model_path',String),                 
                Column('condor_id',String),
                Column('condor_status',String),  
                Column('host',String),                               
                Column('size_g',Float),
                Column('time_update',DateTime),    
                Column('time_start',DateTime),  
                Column('time_queue',DateTime),      
                Column('priority', Integer),
                Column('run_time', DateTime),
                schema='condor')

mapper(JobStatus, simulation_table,  
                    properties={ 'id':  simulation_table.c.id,
                                 'run_name':  simulation_table.c.run_name,
                                 #'model_path':  simulation_table.c.model_path,
                                 'condor_id': simulation_table.c.condor_id,
                                 'condor_status':simulation_table.c.condor_status,
                                 'host': simulation_table.c.host,
                                 'size_g': simulation_table.c.size_g,
                                 'time_update':simulation_table.c.time_update,      
                                 'start_time':simulation_table.c.time_start,  
                                 'queue_time':simulation_table.c.time_queue,       
                                 'priority':simulation_table.c.priority,     
                                 'run_time':simulation_table.c.run_time,                     
                                })     
''' =============================  end of condor        =========================================== ''' 

''' =============================  start of model_meta    =========================================== ''' 
run_table = Table('run', metadata,
                Column('id', Integer, primary_key=True),
                Column('name',String), 
                Column('dir_run',String), 
                               
                Column('archive_required',Boolean),  
                Column('archive_failed',Boolean),                                  
                Column('archive_history',String),
                schema='model_meta')

mapper(Run, run_table,  
                    properties={ 'id':  run_table.c.id,
                                 '_name':  run_table.c.name,
                                 '_dir_run':  run_table.c.dir_run,
                                 '_archive_required':  run_table.c.archive_required,  
                                 '_archive_failed':  run_table.c.archive_failed,
                                 '_archive_history':  run_table.c.archive_history,                 
                                })    


run_archive_table = Table('run_archive', metadata,
                Column('id', Integer, primary_key=True),
                Column('name',String), 
                Column('version',Integer), 
                Column('file_name',String),                            
                Column('comment',String),
                Column('archive_time',DateTime),
                schema='model_meta')

mapper(RunArchive, run_archive_table,  
                    properties={ 'id':  run_archive_table.c.id,
                                 'name':  run_archive_table.c.name,
                                 'version':  run_archive_table.c.version,
                                 'file_name':  run_archive_table.c.file_name,  
                                 'comment':  run_archive_table.c.comment,   
                                 'archive_time':  run_archive_table.c.archive_time,                
                                })    

''' scenario ''' 
scenario_table = Table('scenarios', metadata,
                Column('id', Integer, primary_key=True),
                Column('description',String),
                Column('suffix',String),
                Column('rp',Float),
                Column('defended',Boolean)
                ,schema='model_meta')
 
 
mapper(Scenario,scenario_table  ,  
                    properties={ '_id':  scenario_table.c.id,
                                 '_description' : scenario_table.c.description,
                                '_suffix':  scenario_table.c.suffix,
                                '_rp': scenario_table.c.rp,
                                '_defended':scenario_table.c.defended,
                                })        
''' =============================  end of model_meta    =========================================== '''

 
''' =============================  start of model_gi    =========================================== '''

from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Topography modification
class ZArea(Base):
    __tablename__ = 'zarea'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key=True)
    geom = Column(Geometry('POLYGON',3826))  # LINESTRING  POINT
    height = Column(Float)
    lowest_val = Column(Float)
    comment = Column(String)

class ZLine_Pl(Base):
    __tablename__ = 'zline_pl'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('LINESTRING',3826))
    height = Column(Float,nullable=False,default =-9999.0)
    height1 = Column(Float,nullable=False,default =-9999.0)
    height2 = Column(Float,nullable=False,default =-9999.0)
    thick = Column(Integer)
    intrp_ends = Column(Integer)
    lowest_val = Column(Integer)
    comment = Column(String)

class ZLine_PlPt_Pl(Base):
    __tablename__ = 'zline_plpt_pl'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('LINESTRING',3826))
    height = Column(Float)
    thick = Column(Integer)
    comment = Column(String)

class ZLine_PlPt_Pt(Base):
    __tablename__ = 'zline_plpt_pt'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('LINESTRING',3826))
    height = Column(Float)
    thick = Column(Integer)

# Roughness modification
class NArea(Base):
    __tablename__ = 'narea'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('POLYGON',3826))
    method = Column(VARCHAR(50))
    value = Column(Float)
    comment = Column(String)

# Boundary
class Boundary(Base):
    __tablename__ = 'boundary'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('LINESTRING',3826))
    type = Column(VARCHAR(254))
    value = Column(Float)
    domain_gid = Column(Integer)
    flow_point_gid = Column(Integer)

# Domain
class Domain(Base):
    __tablename__ = 'domain'
    __table_args__ = {'schema' : 'model_gi'}
    gid = Column(Integer, primary_key = True)
    geom = Column(Geometry('POLYGON',3826))
    name = Column(VARCHAR(254))
    domain_ws = Column(VARCHAR(254))
    cell_size = Column(Float)
    us_domain_gids = Column(Integer)
    ds_domain_gids = Column(Integer)
    us_bdy_gids = Column(Integer)
    bs_bdy_gids = Column(Integer)
    ds_end = Column(Boolean)
    modeller = Column(VARCHAR(254))
    reviewer = Column(VARCHAR(254))
    log = Column(String)
    comment = Column(String)
    status = Column(VARCHAR(254))

Base.metadata.create_all(engine)
 
''' =============================  end of model_gi    =========================================== '''
#metadata.create_all(engine)
Session = sessionmaker(bind=engine) 
_session = Session()


