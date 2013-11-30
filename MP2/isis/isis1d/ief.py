import os
from  collections import OrderedDict
from ConfigParser import SafeConfigParser 

#===============================================================================
# ISIS_EVENT_DETAILS = OrderedDict()
# ISIS_EVENT_DETAILS['RunType']='Unsteady'
# 
# ISIS_EVENT_DETAILS['Start']=0
# ISIS_EVENT_DETAILS['Finish']=250
# ISIS_EVENT_DETAILS['Timestep']=5
# ISIS_EVENT_DETAILS['SaveInterval']=3600
# 
# #ISIS_EVENT_DETAILS['EventData']=''
# 
# ISIS_EVENT_DETAILS['Dflood']=6
# ISIS_EVENT_DETAILS['Qtol']=0.005
# ISIS_EVENT_DETAILS['Htol']=0.005
# ISIS_EVENT_DETAILS['Maxitr']=11
# ISIS_EVENT_DETAILS['Minitr']=4
#   
#   
# ISIS_EVENT_DETAILS['Slot']=1
# ISIS_EVENT_DETAILS['ExtraTimesteps']=0
# ISIS_EVENT_DETAILS['ICsFrom']=1
# ISIS_EVENT_DETAILS['RefineBridgeSecProps']=0
# ISIS_EVENT_DETAILS['MathRules']=1
#   
# ISIS_EVENT_DETAILS['SolveDHEqualsZeroAtStart']=1
# ISIS_EVENT_DETAILS['PSTruePerimeter']=1
# ISIS_EVENT_DETAILS['RulesAtTimeZero']=1
# ISIS_EVENT_DETAILS['RulesOnFirstIteration']=0
# ISIS_EVENT_DETAILS['ResetTimesAfterPos']=1
# ISIS_EVENT_DETAILS['UseFPSModularLimit']=1
# ISIS_EVENT_DETAILS['OutputConvergencePlotBMP']=0
# ISIS_EVENT_DETAILS['UseRemoteQ']=0
#===============================================================================

def write_ief(filename,parametersDict):
        
    config = SafeConfigParser()
    
    config.add_section('ISIS Event Header')
    
    config.set('ISIS Event Header','Datafile',parametersDict['Datafile'])
    config.set('ISIS Event Header','Results',parametersDict['Results'])

    config.add_section('ISIS Event Details')
    
    config.set('ISIS Event Details','RunType',parametersDict['RunType'])
    config.set('ISIS Event Details','Start',str(parametersDict['Start']))
    config.set('ISIS Event Details','Finish',str(parametersDict['Finish']))
    config.set('ISIS Event Details','Timestep',str(parametersDict['Timestep']))
    config.set('ISIS Event Details','SaveInterval',str(parametersDict['SaveInterval']))
    
    with open(filename,'wb') as configfile:
        config.write(configfile)
    
def writeIef1(filename,parametersDict):
    if os.path.isfile(filename):
        os.unlink(filename)
    fileObject = open(filename, 'a')
    
    fileObject.write('[ISIS Event Header]')
    fileObject.write('\n')
    fileObject.write('Datafile='+str(parametersDict['Datafile']))
    fileObject.write('\n')
    fileObject.write('[ISIS Event Details]')
    fileObject.write('\n')
    fileObject.write('RunType=Unsteady')
    fileObject.write('\n')
    fileObject.write('Start=0')
    fileObject.write('\n')
    fileObject.write('Finish='+str(parametersDict['Finish']))
    fileObject.write('\n')
    fileObject.write('Timestep='+str(parametersDict['Timestep']))
    fileObject.write('\n')
    fileObject.write('SaveInterval='+str(parametersDict['SaveInterval']))
    fileObject.write('\n')
    fileObject.write('Dflood=20')
    fileObject.write('\n')
    fileObject.write('Htol=0.005')
    fileObject.write('\n')
    fileObject.write('Qtol=0.005')
    fileObject.write('\n')
    fileObject.write('Maxitr='+str(parametersDict['Maxitr']))
    fileObject.write('\n')
    fileObject.write('Slot=1')
    fileObject.write('\n')
    fileObject.write('ExtraTimesteps=0')
    fileObject.write('\n')
    fileObject.write('ICsFrom=1')
    fileObject.write('\n')
    fileObject.write('RefineBridgeSecProps=0')
    fileObject.write('\n')
    fileObject.write('MathRules=1')
    fileObject.write('\n')
    fileObject.write('SolveDHEqualsZeroAtStart=1')
    fileObject.write('\n')
    fileObject.write('PSTruePerimeter=1')
    fileObject.write('\n')
    fileObject.write('RulesAtTimeZero=1')
    fileObject.write('\n')
    fileObject.write('RulesOnFirstIteration=0')
    fileObject.write('\n')
    fileObject.write('ResetTimesAfterPos=1')
    fileObject.write('\n')
    fileObject.write('UseFPSModularLimit=1')
    fileObject.write('\n')
    fileObject.write('OutputConvergencePlotBMP=0')
    fileObject.write('\n')
    fileObject.write('UseRemoteQ=0')
    fileObject.write('\n')

    fileObject.close()
    
    return

if __name__ == '__main__':
    
    parametersDict=dict()
    parametersDict['Datafile']=r'P:\Siret\ISIS2D\Trotus2\1D\Trotus_v5_Tr2.DAT'
    parametersDict['Results']=r'P:\Siret\ISIS2D\Trotus2\1D\TROTUS_2D2_10yr_v2'
       
    parametersDict['RunType']='Unsteady'
     
    parametersDict['Start']=0
    parametersDict['Finish']=250
    parametersDict['Timestep']=5
    parametersDict['SaveInterval']=3600    
    
    write_ief(r'test_files\dom11.ief',parametersDict)