import sys
import os
import subprocess

from osgeo import ogr
import pandas as pd

isisMapper = r"C:\isis\bin\ISISMapper.exe"


def prepare_flow_for_sections(shpXsection, csvFlows,flowTag, csvOutput):

    """
    @summary:  prepare the flows.csv for the normal depth mappting tool 
    @param : 
    
    """
  
    ''' 1. read in the section shapefile '''
    driver = ogr.GetDriverByName("ESRI Shapefile")
    ds = driver.Open(shpXsection, 0)
    vlayerSections=ds.GetLayer(0)
    if ds is None:
        print 'Could not open file:' + shpXsection
        sys.exit(1)
                    
    lstSections = []
    feat = vlayerSections.GetNextFeature()
    while feat:    
                
        label = str(feat.GetField('label'))
        slope = float(feat.GetField('slopeavg'))
        hydroID = long(feat.GetField('HydroID'))

        
        lstSections.append({'HydroID':hydroID,
                            'slope':slope,
                            'label':label})
        
        feat = vlayerSections.GetNextFeature()
    
    dfSections = pd.DataFrame(lstSections)    
    dfSections.index = dfSections['HydroID']
   
    ''' 2. join flow data '''
    dfFlows = pd.read_csv(csvFlows,index_col=['DrainID'],header =0)
    
    dfJoin = dfSections.join(dfFlows)
    dfJoin['flow']=dfJoin[flowTag]
    
    dfOutput = dfJoin.ix[:,['label','HydroID','slope','flow']]
    dfOutput.index.name ='ID'
    dfOutput.to_csv(csvOutput)
    
    print 'end of prepare_flow_for_sections'
    return csvOutput


def CalculateSlope(shpXsection):
    """NB: Input shape file must be of cross section type shape file"""
    try:
        args = '-calculateslope  /i: ',shpXsection
        subprocess.call([isisMapper,args],shell=True)
    except ValueError as e: print(e)


def Calculate_NormalDepth(shpXsection, xSectionFile, csvFlowFile, csvDepthOutput):
    """
    ISISMapper.exe -calculatenormaldepth /i: xs.shp,xs.sec,flows.csv /o: output.csv
    NB: flows.csv must contain first line as header: [label,flow,slope] 
    if ISIS Mapper cannot find the slope or flow in the input csv file, 
    it will look into the attribute table of cross section file.
    """

    try:
        args = '-calculatenormaldepth /i: ',shpXsection+','+xSectionFile+','+csvFlowFile, ' /o: ',csvDepthOutput
        subprocess.call([isisMapper,args],shell=True)
    except ValueError as e: print(e)
    return csvDepthOutput

    
if __name__ == '__main__':
    #shpXsection= r'test_files\xsection.shp'
  #  shpXsection= r'test_files\xsection.shp'
   # csvFlows = r'test_files\adjcatchd3km1_summary.csv'
  #  flowTag='RP100E_IDW_2'
 #   csvOutput=os.path.join(r'test_files',flowTag+'.csv')
  #  prepare_flow_for_sections(shpXsection, csvFlows, flowTag, csvOutput)

    shpXsection= r'test_files\xsection_join.shp'
    csvFlows = r'test_files\adjcatchd3km1_summary.csv'
    flowTag='RP100E_IDW'
    csvOutput=os.path.join(r'test_files',flowTag+'.csv')
    prepare_flow_for_sections(shpXsection, csvFlows, flowTag, csvOutput)