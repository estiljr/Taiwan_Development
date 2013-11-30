import os
import glob
import pandas as pd
import  matplotlib.pyplot  as  plt
import numpy as np
import csv
from isis.isis1d import ied

from data_setup import *
import pprint


def convert_csvs_to_ied(lstRuns,outputFolder,aggr=True):
    """
    @param aggr: if true, one IED file is created for each run with multiple sites
                 if false, each site will generate one IED file.
    """
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)
    
    for run in lstRuns:
        
        csvfiles = glob.glob(run[1]+'/*.csv')
                
        dictTS = dict()
        for csvFile in csvfiles:
            csvFileName =  os.path.split(csvFile)[1]
            #siteName = 'B'+csvFileName.split('_')[1].split('.')[0]
            siteName = csvFileName.split('_')[1].split('.')[0]
            
            
            
            fo = open(csvFile)
            data = csv.DictReader(fo)
            
            timeValuePairs = list()
            for line in data:
                time = float(line['Time(hours)'])
                value= float(line['Flow Hydrograph'])
                #print time,value    
                timeValuePairs.append((time,value))
            dictTS[siteName] = timeValuePairs
            
            if not aggr:
                subOutputDir = os.path.join(outputFolder,run[0])
                if not os.path.isdir(subOutputDir):
                    os.makedirs(subOutputDir)
                outputFile =os.path.join(subOutputDir,siteName+'.ied')
                ied.write_ied_boundary(outputFile,dictTS,'QTBDY')
                dictTS = dict()
        if aggr:
            outputFile = os.path.join(outputFolder,run[0]+'.ied')
            ied.write_ied_boundary(outputFile,dictTS,'QTBDY')


def aggregate_event_csvs(inputDir,outputFile='adjcatchd3km1_summary.csv'):
    csvfiles = glob.glob(inputDir+'/adj*peak.csv')
    lstPeakFlows  = []
    for csvFile in csvfiles:
        #print csvFile
        eventName = '_'.join(os.path.split(csvFile)[1].split('_')[1:3])
        dfPeakflow = pd.read_csv(csvFile,header=None,index_col=0,names=['DrainID',eventName]) 
        lstPeakFlows.append(dfPeakflow)
    
    dfPeakFlows = pd.concat(lstPeakFlows,axis=1)
    #print dfPeakFlows.head(3)
    dfPeakFlows.to_csv(os.path.join(inputDir,outputFile))
    
    
            
def aggregate_point_csvs(lstRuns,outputFolder):
    """
    @summary: 1. it aggregates all individual (per site per RP) csv results from ISIS hydrology into a single csv files as per event.
              2. it also generates a summary report of peak flows as per event
    """
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)
    
    for run in lstRuns:
        flowSeries = []
        
        csvfiles = glob.glob(run[1]+'/*.csv')
        outputFile_TS = os.path.join(outputFolder,run[0]+'_ts.csv')
        outputFile_Peak = os.path.join(outputFolder,run[0]+'_peak.csv')
        for csvFile in csvfiles:
    
            csvFileName =  os.path.split(csvFile)[1]
            
            if csvFileName == run[0]+'.csv':
                continue
            siteName = csvFileName.split('_')[-1].split('.')[0]
            #print csvFileName,siteName,csvFile
            flows = pd.read_csv(csvFile,index_col ='Time(hours)')['Flow Hydrograph']        
            flows.name = siteName
            flowSeries.append(flows)        
    
        dfFlowSeries = pd.concat(flowSeries,join='outer',axis=1)
        sPeakFlows = dfFlowSeries.max(0)
        sPeakFlows.index.name = 'site'
        sPeakFlows.name = 'peakFlow'
        sPeakFlows.to_csv(outputFile_Peak) #TODO: need to add site, flow to heading. above does not work
        dfFlowSeries.to_csv(outputFile_TS)
                        
def generate_plots_for_multiple_RPs_for_multiple_sites(lstRuns,outputFolder):
    """
    @note: it calls method: plot_multiple_hydrographs_for_single_site()
    """    
    if not os.path.isdir(outputFolder):
        os.makedirs(outputFolder)

    csvfiles = glob.glob(lstRuns[0][1]+'/*.csv')
    
    for csvFile in csvfiles:
        dictCatchment = dict()
        dictCatchment[lstRuns[0][0]]=csvFile
        
        csvFileName =  os.path.split(csvFile)[1]
#         if csvFileName == run[0]:
#             continue
        print csvFileName
                           
        for i in range(1,4):
            fn =  os.path.join(lstRuns[i][1],csvFileName.replace(lstRuns[0][0],lstRuns[i][0]))
            dictCatchment[lstRuns[i][0]]=fn
        
        plot_multiple_hydrographs_for_single_site(dictCatchment,csvFileName.split('_')[1].split('.')[0],outputFolder) 
        
def plot_multiple_hydrographs_for_single_site(dictFiles,title,outputFolder='./'):
    #dictFiles = {series lable: file name}
    flowSeries = []
    for k in dictFiles.keys():
        #flows = pd.read_csv(dictFiles[k],index_col ='Time(hours)')['Flow Hydrograph']        
        #flows.name = k
        flows = pd.read_csv(dictFiles[k]) 
        #flowSeries.append(flows)
        #print flows
        if 'Exist' in k:
            marker = '*'
            ls = '-'
        else:
            marker = 'o'
            ls = '--'
        plt.plot(flows['Time(hours)'],flows['Flow Hydrograph'],label = k,marker = marker,ls=ls)
        plt.hold(True)
        
    plt.hold(False)    
    plt.legend(loc='best')
    plt.title('Drainage ID: '+title)
    plt.xlabel('time (hrs)')
    plt.ylabel('flow (m3/s)')
    plt.savefig(os.path.join(outputFolder,title+'.png'))
    #dfFlowSeries = pd.concat(flowSeries,join='outer')
    #print dfFlowSeries
    

def compare_flows_between_different_methods():
    """
    @summary: it takes the peak flow summary from aggregate_event_csvs()
              compare two sets of flow estimates for the same catchments.
    """
    csvIDWFiles = glob.glob(r'take_home/*IDW*peak.csv')
    lstDiffs =[]
    for csvIDW in csvIDWFiles:    
        csvKRG = csvIDW.replace('IDW','KRG')
        #print csvIDW, csvKRG
        dfSingleIDW = pd.read_csv(csvIDW,index_col=0,names=['DrainageID','IDW'])
        dfSingleKRG = pd.read_csv(csvKRG,index_col=0,names=['DrainageID','KRG'])
        dfSiggleDiff = pd.concat([dfSingleIDW,dfSingleKRG],axis=1)
        lstDiffs.append(dfSiggleDiff)
    
    dfDiff = pd.concat(lstDiffs,ignore_index=True, axis=0)
    dfDiff['Diff']=dfDiff['KRG'] - dfDiff['IDW']
    
    dfDiff['ratio']=(dfDiff['KRG']/dfDiff['IDW'])
    dfDiff['ratio'].hist(alpha=0.5, bins=50,normed=True)
    plt.title('Distribution of flow ratio (KRG/IDW)')
    plt.xlabel('KRG/IDW')
    plt.savefig('Distribution_of_flow_ratio.png')
    
    
    bins = [0, 100, 200,1000,10000]
    cats = pd.cut(dfDiff['IDW'], bins,right=False) 
    dfDiff['cat']=cats.labels
    
    dfDiff.to_csv('flow_diff.csv')
    
    
    fig, axes = plt.subplots(nrows=2, ncols=2,figsize=(10, 8))
    dfDiff[dfDiff['cat']==0]['Diff'].hist(alpha=0.5, bins=50,normed=True,ax=axes[0,0])
    axes[0,0].set_title('IDW flows within ' + str(cats.levels[0]))
    dfDiff[dfDiff['cat']==1]['Diff'].hist(alpha=0.5, bins=50,normed=True,ax=axes[0,1])
    axes[0,1].set_title('IDW flows within ' + str(cats.levels[1]))
    dfDiff[dfDiff['cat']==2]['Diff'].hist(alpha=0.5, bins=50,normed=True,ax=axes[1,0])
    axes[1,0].set_title('IDW flows within ' + str(cats.levels[2]))
    dfDiff[dfDiff['cat']==3]['Diff'].hist(alpha=0.5, bins=50,normed=True,ax=axes[1,1])
    axes[1,1].set_title('IDW flows within ' + str(cats.levels[3]))
    plt.xlabel('KRG -IDW (m3/s)')
    plt.savefig('flow_diff_subplots.png')
    
if __name__ == '__main__':
    lstRuns=[ ['catchd3km1_RP100E_IDW' ,
               r'C:\temp\taiwan\scs\ISISHydrology\catchd3km1_RP100E_IDW']              
            ]
    
    outputFolder = r'C:\temp\taiwan\111\scs\scs_summary'

    #generate_plots_for_multiple_RPs_for_multiple_sites()
    #plot_multiple_hydrographs_for_single_site(tst,'21394')
    
    #convert_csvs_to_ied(lstRuns,outputFolder,False)
    
#===============================================================================
#     lstRuns = []
#     
#     for k,dataConfig in rainData.items():
#         InFCName =  runSCSData['input']['catchment_name']
#         rainfallZonalOutput = InFCName + '_' + dataConfig['oGrid']
# 
#         dirOutput = os.path.join(runSCSData['output']['output_scs_ws'],dataConfig['oGrid'],InFCName)
#         
#         lstRuns.append([rainfallZonalOutput,dirOutput])
#         
#     pprint.pprint(lstRuns)
#     aggregate_point_csvs(lstRuns,outputFolder)
#===============================================================================

    aggregate_event_csvs( r'C:\temp\taiwan\111\scs\scs_summary')