import os
import subprocess
import datetime
import time

import sys
import mp2
#from mp2.utility import errors

from lxml import etree  # @UnresolvedImport
from collections import defaultdict

#print time.strftime('%d/%m/%Y %H:%M:%S ') + ': poolInfoAdv - Executed successfully'

"""
condor_submit : no condor id
condor_q global: I, R,C, H 
condor_history: looping from the last condor_id to increment till finished
"""

class CondorSystem(object):

    def __init__(self, dbConn=None):
        CONDOR_BIN_FOLDER = r'c:\condor\bin'
        
        self.EXE_CONDOR_STATUS = os.path.join(CONDOR_BIN_FOLDER, 'condor_status.exe')
        self.EXE_CONDOR_Q = os.path.join(CONDOR_BIN_FOLDER, 'condor_q.exe')
        self.EXE_CONDOR_SUBMIT = os.path.join(CONDOR_BIN_FOLDER, 'condor_submit.exe')
        self.EXE_CONDOR_RM = os.path.join(CONDOR_BIN_FOLDER, 'condor_rm.exe')
        self.EXE_CONDOR_PRIO= os.path.join(CONDOR_BIN_FOLDER, 'condor_prio.exe')
        
        self.__dbConn = dbConn
         
    def ret_slots_no(self):
        """
        @summary:  # return a dict consist of the number of slots for various categories
        
        @note
                        Total Owner Claimed Unclaimed Matched Preempting Backfill
               Total    68     8       0        60       0          0        0
        """
        
        p1 = subprocess.Popen(self.EXE_CONDOR_STATUS, stdout = subprocess.PIPE)
        out, err = p1.communicate(input = None)
        p1.wait()
        lines = out.split('\n')
        slotNoList = lines[-2].split()
        slots = dict()
        slots['total'] = int(slotNoList[1])
        slots['owner'] = int(slotNoList[2])
        slots['claimed'] = int(slotNoList[3])
        slots['unclaimed'] = int(slotNoList[4])
        return slots
    
    def ret_jobs_no(self):
        """
        @return: a dict consist of number of global Condor jobs for various categories
                 none if empaty
        """
           
        p1 = subprocess.Popen(self.EXE_CONDOR_Q + ' -global', stdout = subprocess.PIPE)
        
        out, err = p1.communicate(input = None)
        p1.wait()

        #===========================================================================
        #98 jobs; 17 idle, 81 running, 0 held
        #===========================================================================

        lines = out.split(os.linesep)
        if len(lines)<3:
            return
        else:
            jobs = dict()
            
            jobNoLine = lines[-2].split(' ')
            print jobNoLine
            jobs['total'] =jobNoLine[0]
            jobs['idle'] =jobNoLine[2]
            jobs['running'] =jobNoLine[4]
            jobs['held'] =jobNoLine[6]
            return jobs
            
    def get_slot_list(self):
        """
        @summary:  Gather and update the advanced slots and client pc info 
        @return:   a list of slot object and a list of client object
        """
                
        #======================================================================
        # <a n="Name"><s>slot2@W024204.amr.ch2m.com</s></a>
        # <a n="Machine"><s>W024204.amr.ch2m.com</s></a>
        # <a n="CondorVersion"><s>$CondorVersion: 7.4.4 Oct 13 2010 BuildID: 279383 $</s></a>
        #<a n="TotalDisk"><i>73714400</i></a>   # total available in the system
        #<a n="Disk"><i>36857200</i></a>        # distributed by the cores
#         <a n="LoadAvg"><r>4.099999964237213E-001</r></a>
#         <a n="KeyboardIdle"><i>441533</i></a>
#         <a n="ConsoleIdle"><i>441533</i></a>
#         <a n="Memory"><i>4094</i></a>         # available for each core
#     <a n="Arch"><s>INTEL</s></a>
#     <a n="OpSys"><s>WINNT61</s></a>
#     <a n="KFlops"><i>1341037</i></a>
#     <a n="Mips"><i>6127</i></a>
#     <a n="TotalSlots"><i>2</i></a>    
#     <a n="State"><s>Claimed</s></a>
        #======================================================================
        
        lstSlots =[] 
        lstClients=[]
        
        p1 = subprocess.Popen(self.EXE_CONDOR_STATUS + ' -xml', stdout = subprocess.PIPE)
        out, err = p1.communicate(input = None)
        p1.wait()
        #print out
        try:
            root=etree.XML(out)
        except:
            # no job running
            return
    
        for slot in root:
            slotInfo = defaultdict(dict)                
            for element in slot.iter():
                attrText = element.get('n')
                if attrText is not None:
                    slotInfo[attrText]=element[0].text
            
            objSlot = Slot(slotInfo)
            objClient = Client(slotInfo)
            lstSlots.append(objSlot) 
            lstClients.append(objClient)
            #print slotInfo            
        return lstSlots, lstClients
                     
    def set_priority(self, condor_id, priority):
        """
        @summary: set the priority for the specified condor job
        """
        if priority > 20:
            priority = 20
        if priority < -20:
            priority = -20

        CMD = [self.EXE_CONDOR_PRIO, "-p" , str(priority), str(condor_id)]
        p1 = subprocess.Popen(CMD, stdout = subprocess.PIPE)
        out, err = p1.communicate(input = None)
        p1.wait()
       


   
    def get_condor_q(self):
        """
        @summary:  Gather the queque status via condor_q -global
        @return:   a list of JobStatus object 
                    None if there is no jobs in the queue
        """
        #condor_q -global -xml
        #=======================================================================
        # <c>
        #     <a n="ClusterId"><i>81132</i></a>
        #     <a n="User"><s>jiy@ch2m.com</s></a>
        #     <a n="QDate"><i>1371969983</i></a>
        #     <a n="Iwd"><s>E:\Models\RunningModels\Ha012_Cat0037_Dom044_10Yr_D_S_BLOC</s></a>
        #     <a n="Cmd"><s>E:\Models\RunningModels\Ha012_Cat0037_Dom044_10Yr_D_S_BLOC\bootStrap.bat</s></a>           
        #     <a n="UserLog"><s>E:\Models\RunningModels\Ha012_Cat0037_Dom044_10Yr_D_S_BLOC\slave.log</s></a>
        #     <a n="In"><s>/dev/null</s></a>
        #     <a n="TransferIn"><b v="f"/></a>
        #     <a n="Out"><s>slave.out</s></a>
        #     <a n="StreamOut"><b v="f"/></a>
        #     <a n="Err"><s>slave.err</s></a>
        #     <a n="GlobalJobId"><s>SWIN-AS-20.amr.ch2m.com#81132.0#1371969983</s></a>
        #     <a n="StartdPrincipal"><s>10.124.121.2</s></a>        
        #    <a n="JobStartDate"><i>1385386860</i></a>
        #    <a n="JobCurrentStartDate"><i>1385386860</i></a>   
        #     <a n="JobPrio"><i>0</i></a>                  priority
        #     <a n="DiskUsage_RAW"><i>1017103</i></a>
        #     <a n="DiskUsage"><i>1250000</i></a>
        #     <a n="RemoteWallClockTime"><r>3.665100000000000E+004</r></a>
        #     <a n="LastRemoteHost"><s>slot1@UKE7T1TH5J.amr.ch2m.com</s></a>
        #     <a n="CurrentHosts"><i>0</i></a> <a n="CurrentHosts"><i>1</i></a> for running model
        #     <a n="RemoteHost"><s>slot12@UKSFZWTD5J.amr.ch2m.com</s></a> none, it is not running?
        #=======================================================================


        #===============================================================================
        # history 
        
        # <a n="ImageSize"><i>12500</i></a>
        # <a n="ExitCode"><i>0</i></a>
        # <a n="CompletionDate"><i>1385387170</i></a>
        # <a n="JobFinishedHookDone"><i>1385387170</i></a>
        # <a n="LastRemoteHost"><s>slot2@UKS9RRTD5J.amr.ch2m.com</s></a>
        # <a n="JobStatus"><i>2</i></a>
        # 
        #===============================================================================
       
        p1 = subprocess.Popen(self.EXE_CONDOR_Q + ' -global -xml', stdout = subprocess.PIPE)
        out, err = p1.communicate(input = None)
        p1.wait()
        #print out
        try:
            root=etree.XML(out)
        except:
            # no job running
            return
        
        lstJobStatus =[] 
        
        for job in root:

            jobInfo = defaultdict(dict)                
            for element in job.iter():
                attrText = element.get('n')
                if attrText is not None:
                    jobInfo[attrText]=element[0].text
            
            objJobStatus = JobStatus(jobInfo) 
            lstJobStatus.append(objJobStatus)
        return lstJobStatus

    def condor_rm(self, condorId):
        """ Cancel a CONDOR job. using condorID (e.g. 100.0)"""
        try:
            sIn = open(os.devnull, 'r')
            p = subprocess.Popen([self.EXE_CONDOR_RM, condorId], stdin = sIn, stderr = sys.stderr, stdout = sys.stderr)
            rtn = p.wait()
            sIn.close()
            if rtn != 0:
                erMsg = 'Failed to remove job ' + condorId + ' from the cluster, return was ' + str(rtn)
                #self.__log(erMsg)
                #raise errors.CondorError(erMsg)
        except:
           pass
            #erMsg = 'Failed to remove job ' + condorId + ' from the cluster, unknown exception was ' + s
            #self.__log(erMsg)
            #raise errors.Error(erMsg)


class Client(object): 
    def __init__(self,dictSlot):
        self.id=None
        self.name = dictSlot['Machine']        
        self.version= dictSlot['CondorVersion']
        self.arch= dictSlot['Arch']
        self.os= dictSlot['OpSys']  
        self.version =  dictSlot['CondorVersion']  
        self.slots= dictSlot['TotalSlots']
        self.run_count = None
                
class Slot(object):
    def __init__(self,dictSlot):
        self.id =None
        self.name = dictSlot['Name']
        self.state= dictSlot['State'] 
        
        self.machine= dictSlot['Machine']

        if len(dictSlot['KFlops'])==0:
            self.kflops= -9999
        else:
            self.kflops= int(dictSlot['KFlops'])
            
        
        if len(dictSlot['Mips'])==0:
            self.mips= -9999
        else:
            self.mips = dictSlot['Mips']
             
        self.disk= long(dictSlot['Disk'])/1024/1024.0
        self.memory= long(dictSlot['Memory'])/1024.0
        self.loadav = float(dictSlot['LoadAvg'])
            

class JobStatus(object):

    def __init__(self, dictJob):
        #print dictJob['User']
        self.time_update = datetime.datetime.now()
                                           
        self.condor_id =  str(dictJob['ClusterId'])
        
        if len(dictJob['RemoteHost'])>0:
            self.host =  dictJob['RemoteHost']
        else:
            self.host = None
        
        
        self.priority = int(dictJob['JobPrio'])
        
        self.run_name = os.path.split(dictJob['Iwd'])[-1]
        
        if len(dictJob['DiskUsage'])>0:
            self.size_g = long(dictJob['DiskUsage'])/1024.0/1024.0
        else:
            self.size_g  = None
        
        #print dictJob['JobCurrentStartDate']
        
        if len(dictJob['JobCurrentStartDate']) > 0:
            self.start_time= datetime.datetime.fromtimestamp(long(dictJob['JobCurrentStartDate']))
            self.run_time = self.time_update-self.start_time
            print self.run_time
        else:
            self.start_time = None
            self.run_time = None
        
        
        if len(dictJob['QDate']) > 0:
            self.queue_time = datetime.datetime.fromtimestamp(long(dictJob['QDate']))
        else:
            self.queue_time = None
        #datetime.datetime.fromtimestamp(long(dictJob['JobStartDate']))
        
        iJobStatus = int(dictJob['JobStatus'])
        # 0    Unexpanded     U
        # 1    Idle     I
        # 2    Running     R
        # 3    Removed     X
        # 4    Completed     C
        # 5    Held     H
        # 6    Submission_err     E
        
        if iJobStatus==1:
            self.condor_status = 'idle'
        elif iJobStatus==2:
            self.condor_status = 'running'
        elif iJobStatus==4:
            self.condor_status = 'completed'
        elif iJobStatus==5:
            self.condor_status = 'held'            
        else:
            self.condor_status = 'unknown' 


class CondorLog(object):
    """
    @summary: class processing the log file returned by condor
    """
    def __init__(self, fnLog):
        self._fnLog = fnLog
    
    def get_status_retcode(self):
        
        """
        @return a tuple of (status, retCode): 
                status: 
                    'error' - model file missing; 
                    'running' - ; 
                    'terminated' - coupled with retCode 
                    'cancelled' -
                    'submitted' - just submitted, but not running
                retCode: 100, 102, 103, etc
        """
        status = None
        retCode = None
        
        if not os.path.isfile(self._fnLog):
            #self.__logger.info('[%s]  CONDOR log file missing ' % self._fnLog)
            return 'error', retCode
        
        #=======================================================================
        # 001 (78242.000.000) 06/12 09:03:54 Job executing on host: <10.101.125.106:1150>
        # ...
        # 005 (78242.000.000) 06/12 10:41:20 Job terminated.
        #     (1) Normal termination (return value 112)
        #=======================================================================
        
        f = open(self._fnLog, 'r')
        # read the file from bottom
        for line in reversed(f.readlines()): 
            if 'Normal termination' in line:
                retCode = int(line.split(' ')[-1][:-2])               
                status = 'terminated'
                break
            elif 'Abnormal termination' in line:
                retCode = int(line.split(' ')[-1][:-2])               
                status = 'terminated'
                break           
            elif 'Job executing' in line:
                status = 'running'
                retCode = None
                break
            elif '000' == line[:3]:
                #000 (87439.000.000) 07/02 15:32:49 Job submitted from host: <10.101.10.71:8080>
                status = 'submitted'
                retCode = None
                break
            
            elif '009' == line[:3]:
                status = 'cancelled'
                retCode = None
                break
        f.close()
        return status, retCode
        
        
        
if __name__ == '__main__':
    objCondor = CondorSystem()
    #print objCondor.ret_slots_no()
    #print objCondor.ret_jobs_no()
    #print objCondor.get_condor_q()
    #print objCondor.get_slot_list()

    for objCondorJob in objCondor.get_condor_q():
        print objCondorJob