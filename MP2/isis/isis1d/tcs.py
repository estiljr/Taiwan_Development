import os
import subprocess as sp
from ConfigParser import SafeConfigParser

#C:\isis\bin\Tabularcsv.exe -silent -tcs "c:\isis\data\mytcsfile.tcs" "c:\isis\data\myresultsfile.zzn"

#===============================================================================
# [Data]
# OutputOption=1
# DataItem=0
# ColumnPerNode=0
# OutputTimeUnits=1
# MaxOverOutputInterval=0
# [Times]
# FirstOutputTimeID=-1
# LastOutputTimeID=-1
# OutputInterval=1
# [Nodes]
# Count=814
# Node1=Valea_Rece
# Node2=Lunca_de_Sus
# Node3=Un_GhimesF
#===============================================================================

def write_tcf(filename,parametersDict=None):
    
    if parametersDict is None:
        parametersDict=dict()
        
        parametersDict['OutputOption']=1
        parametersDict['DataItem']=0
        parametersDict['ColumnPerNode']=0
        parametersDict['OutputTimeUnits']=1
        parametersDict['MaxOverOutputInterval']=0 
                
        parametersDict['FirstOutputTimeID']=-1
        parametersDict['LastOutputTimeID']=-1
        parametersDict['OutputInterval']=1    
            
    config = SafeConfigParser()
    
    config.add_section('Data')
    
    config.set('Data','OutputOption',str(parametersDict['OutputOption']))
    config.set('Data','DataItem',str(parametersDict['DataItem']))
    config.set('Data','ColumnPerNode',str(parametersDict['ColumnPerNode']))
    config.set('Data','OutputTimeUnits',str(parametersDict['OutputTimeUnits']))
    config.set('Data','MaxOverOutputInterval',str(parametersDict['MaxOverOutputInterval']))
    
    config.add_section('Times')
    
    config.set('Times','FirstOutputTimeID',str(parametersDict['FirstOutputTimeID']))
    config.set('Times','LastOutputTimeID',str(parametersDict['LastOutputTimeID']))
    config.set('Times','OutputInterval',str(parametersDict['OutputInterval']))
    
    config.add_section('Nodes')
    
    with open(filename, 'wb') as configfile:
        config.write(configfile)


if __name__ == '__main__':
    write_tcf('test_files/tro.tcs')
    
    #.zzn needs other accompanying file
    #result csv file is same as .zzn
    cmd =[r'C:\isis\bin\Tabularcsv.exe', '-silent', '-tcs', 
          r'test_files/t2.tcs', r'test_files/TROTUS_2D2_2005_V2.zzn']
    
    proc = sp.Popen(cmd)
    #proc.wait()
    #print proc.returncode
    out, err = proc.communicate()
    print out,err
    
    
    