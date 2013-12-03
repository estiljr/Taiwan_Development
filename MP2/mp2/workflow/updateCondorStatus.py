
from condor.condor import Slot,Client,JobStatus, CondorSystem



import datetime
import os
from mp2.model.db import _session
from mp2.model.run import Run

#TODO: run mmodel count is not right for pool

def create_new_run(_session):
    objRun = Run('Ha001_Cat0001_Dom001_5Yr_D')
    objRun._dir_run =r'C:\temp\taiwan\model_store\Ha001_Cat0001_Dom001\Ha001_Cat0001_Dom001_5Yr_D'
    objRun._archive_required = True
    _session.add(objRun)
    _session.commit()
    

    
# for objRunNeedsArchive in _session.query(Slot).order_by(Slot.name):
#     print objRunNeedsArchive.name

def update_condor_job_status(_session):    
    """
    @summary:  update condor.simulation table using condor_q
    """
    try:
        objCondor = CondorSystem()
        jobList = objCondor.get_condor_q()
        
        ''' clear all records in system '''
        _session.query(JobStatus).delete()
        
        if jobList is None:
            print 'no job in the queue'
            return
       

       
        ''' add new records '''
        for objCondorJob in jobList:
            _session.add(objCondorJob)    
        
        _session.commit()
        print 'END'
    except:
        print 'error in update_condor_job_status'
        
def update_condor_pool_slots(_session):    
    """
    @summary: update the condor.client and condor.slot table
    """
    objCondor = CondorSystem()
    lstSlots, lstClients = objCondor.get_slot_list()
    
    ''' update slots '''
    for objSlot in lstSlots:
        slotTbl = _session.query(Slot).filter_by(name=objSlot.name).first() 
        if not slotTbl:
            _session.add(objSlot)
        else:
            slotTbl.state = objSlot.state
            slotTbl.loadav = objSlot.loadav
            slotTbl.memory_g = objSlot.memory
            slotTbl.disk_g = objSlot.disk
            slotTbl.mips = objSlot.mips
            slotTbl.kflops = objSlot.kflops        
    _session.commit()
    
        
    ''' update clients '''
    for objClient in lstClients:
        # work out the models running for each machine
        objClient.run_count =  _session.query(Slot).filter_by(machine=objClient.name).filter_by(state='Unclaimed').count() 
        
        ClientTbl = _session.query(Client).filter_by(name=objClient.name).first() 
        
        if not ClientTbl:
            _session.add(objClient)
        else:
            ClientTbl.name = objClient.name
            ClientTbl.os = objClient.os
            ClientTbl.arch = objClient.arch
            ClientTbl.slots = objClient.slots
            ClientTbl.run_count = objClient.run_count   
    _session.commit()

if __name__ == '__main__':
    update_condor_job_status(_session)
    update_condor_pool_slots(_session)
    #
    #archive_models(_session)
        