from ConfigParser import SafeConfigParser
from collections import defaultdict
import sys
import logging
import logging.handlers
import datetime
import time
import os

def logMethod(func):
    
    def log(*args,**kwargs):
        logger = logging.getLogger('mp2.'+func.__name__)
        logger.info ('Starting -' + func.__name__)
        logger.info (args)
        return func(*args,**kwargs)    
        logger.info('Existing -' + func.__name__) #never initiated
    return log

@logMethod
def read_config(fileName):
    """
    @summary: read in config file and translate it into dictionary
    @error:   it will throw error from ConfigParser, and it should stop the system
    """
    configDict = defaultdict(dict)
    
    parser = SafeConfigParser()    
    parser.read(fileName)
    
    configDict['database']['host']= parser.get('database', 'host')
    configDict['database']['port']= parser.get('database', 'port')
    configDict['database']['dbname']= parser.get('database', 'dbname')
    configDict['database']['user']= parser.get('database', 'user')
    configDict['database']['pass']= parser.get('database', 'pass')
    
    configDict['file_system']['condor_template']= parser.get('file_system', 'condor_template')
    configDict['file_system']['log_dir']= parser.get('file_system', 'log_dir')
    configDict['file_system']['backup_dir']= parser.get('file_system', 'backup_dir')
    configDict['file_system']['model_store']= parser.get('file_system', 'model_store')
    configDict['file_system']['running_sim_dir']= parser.get('file_system', 'running_sim_dir')
    configDict['file_system']['ic_root_dir']= parser.get('file_system', 'ic_root_dir')
    configDict['file_system']['topo_root_dir']= parser.get('file_system', 'topo_root_dir')
    configDict['file_system']['roughness_root_dir']= parser.get('file_system', 'roughness_root_dir')
    configDict['file_system']['skeleton_xml_file']= parser.get('file_system', 'skeleton_xml_file')        
    configDict['file_system']['qgs_skeleton_scenario']= parser.get('file_system', 'qgs_skeleton_scenario')
    configDict['file_system']['qgs_skeleton_domain']= parser.get('file_system', 'qgs_skeleton_domain')
    configDict['file_system']['condor_dir']= parser.get('file_system', 'condor_dir')   
    
    
    configDict['exe']['7za']= parser.get('exe', '7za')
    configDict['exe']['isis2d_to_asc']= parser.get('exe', 'isis2d_to_asc')
    configDict['exe']['tabular_csv']= parser.get('exe', 'tabular_csv')
    
    configDict['automation']['wait_time_between_loop_mins']= parser.getfloat('automation', 'wait_time_between_loop_mins')
    configDict['automation']['cancel_all_jobs']= parser.getboolean('automation', 'cancel_all_jobs')
    configDict['automation']['submit_jobs']= parser.getboolean('automation', 'submit_jobs')
    
            
    return configDict


''' Set up the logging '''

cwd = os.path.split(__file__)[0]


#logger = logging.getLogger(__name__)
logger = logging.getLogger('mp2')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
today = datetime.date.today()
#    maxBytes = 100MB backupCount??
fh = logging.handlers.RotatingFileHandler(os.path.join(cwd,'MP_RunLog_'+str(today)), maxBytes=10**8, backupCount=6)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %I:%M:%S')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')


configDict=read_config(os.path.join(cwd,'setting.cfg'))
    
# try:
#     while True:
#         configDict=read_config('setting.cfg')
#         logger.info(configDict)
#         time.sleep(configDict['automation']['wait_time_between_loop_mins']*60)
# except Exception,e:
#     errorCode =1
#     logger.critical('error code: [%s]  error message: [%s]' %(errorCode,e))    
#     sys.exit(errorCode)    
