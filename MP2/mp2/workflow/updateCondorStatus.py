
from condor.condor import Slot,Client,JobStatus, CondorSystem
from mp2.model.run import Run, RunArchive


import datetime
import os
from mp2.model.db import session


def create_new_run(session):
    objRun = Run('Ha001_Cat0001_Dom001_5Yr_D')
    objRun._dir_run =r'C:\temp\taiwan\model_store\Ha001_Cat0001_Dom001\Ha001_Cat0001_Dom001_5Yr_D'
    objRun._archive_required = True
    session.add(objRun)
    session.commit()
    
def archive_models(session):
    """
    @summary: archive as per 'archive_required' column in run table
    @note:
            1) archive the model using the incremental version number from table run_archive
            2)  if successful:
                    a) insert records into run_archive
                    b) update run table
                        'archive_required' - set to false
                        'archive_msg'  - clear text 
                        'archive_history' - append to the history
                else:
                        'archive_required' and 'archive_msg' remain the same
                        'archive_failed' - set to true
                        'archive_history' -  append fail_message                   
    """
    
    for objRunNeedsArchive in session.query(Run).filter_by(_archive_required=True):
        runName =  objRunNeedsArchive._name   
        
        res = session.query(RunArchive).filter_by(name=runName).order_by(RunArchive.version)

        if res.count() ==0:
            newVersion = 1
        else:
            newVersion = res[-1].version +1
        
        
        archive_folder = r'C:\temp\taiwan\model_archive'
        
        objRunArchive = RunArchive()
        objRunArchive.name = runName
        
        objRunArchive.version = newVersion
        objRunArchive.file_name = os.path.join(archive_folder,runName+'_v'+str(newVersion)+'.zip')
        objRunArchive.archive_time = datetime.datetime.now()
        objRunArchive.comment = runName
        
        if True:
            objRunNeedsArchive._archive_required = False;
                    
            if objRunNeedsArchive._archive_msg is None:
                objRunNeedsArchive._archive_msg = 'archived successfully as v[%s] at [%s];' %(newVersion,datetime.datetime.now())
            else:
                objRunNeedsArchive._archive_msg += 'archived successfully as v[%s] at [%s];' %(newVersion,datetime.datetime.now())
        else:
            pass
        session.add(objRunArchive)
    session.commit()
    
# for objRunNeedsArchive in session.query(Slot).order_by(Slot.name):
#     print objRunNeedsArchive.name

def update_condor_job_status(session):    
    """
    @summary:  update condor.simulation table using condor_q
    """
    try:
        objCondor = CondorSystem()
        jobList = objCondor.get_condor_q()
        if jobList is None:
            print 'no job in the queue'
            return
       
        ''' clear all records in system '''
        session.query(JobStatus).delete()
       
        ''' add new records '''
        for objCondorJob in jobList:
            session.add(objCondorJob)    
        
        session.commit()
        print 'END'
    except:
        print 'error in update_condor_job_status'
        
def update_condor_pool_slots(session):    
    """
    @summary: update the condor.client and condor.slot table
    """
    objCondor = CondorSystem()
    lstSlots, lstClients = objCondor.get_slot_list()
    
    ''' update slots '''
    for objSlot in lstSlots:
        slotTbl = session.query(Slot).filter_by(name=objSlot.name).first() 
        if not slotTbl:
            session.add(objSlot)
        else:
            slotTbl.state = objSlot.state
            slotTbl.loadav = objSlot.loadav
            slotTbl.memory_g = objSlot.memory
            slotTbl.disk_g = objSlot.disk
            slotTbl.mips = objSlot.mips
            slotTbl.kflops = objSlot.kflops        
    session.commit()
    
        
    ''' update clients '''
    for objClient in lstClients:
        # work out the models running for each machine
        objClient.run_count =  session.query(Slot).filter_by(machine=objClient.name).filter_by(state='Unclaimed').count() 
        
        ClientTbl = session.query(Client).filter_by(name=objClient.name).first() 
        
        if not ClientTbl:
            session.add(objClient)
        else:
            ClientTbl.name = objClient.name
            ClientTbl.os = objClient.os
            ClientTbl.arch = objClient.arch
            ClientTbl.slots = objClient.slots
            ClientTbl.run_count = objClient.run_count   
    session.commit()

if __name__ == '__main__':
    update_condor_pool_slots(session)
    #update_condor_job_status(session)
    #archive_models(session)
        