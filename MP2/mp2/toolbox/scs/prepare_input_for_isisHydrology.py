from osgeo import ogr
import pandas as pd
import matplotlib.pyplot as plt

import os
import csv
from  collections import defaultdict
import sys
import subprocess


from data_setup import *

''' 
This module is separated from the xxxx_shp_qgis module as the osgeo package seems to be conflict with qgis 

Preparation needed before running prepare_cat_slope_flowLen_Outlet()
     0 ) set up the referernce to the input data within data_setup.py
     1 ) derive catchment slope from zonal_slope()
     2 ) derive CN from calc_cn_from_landuse_intersected() which needs the landuse intersected catchments
     3 ) derive rainfall from derive_rainfall_depth_grids() and zonal_rainfall()

Lastly:
    1) run  prepare_cat_slope_flowLen_Outlet()
    2) run  derive_scs_model_using_rainfall()
'''
os.environ['GDAL_DRIVER_PATH'] = r'C:\OSGeo4W\bin\gdalplugins'
os.environ['GDAL_DATA'] = r'C:\OSGeo4W\share\gdal'


if fileType=='SHP':
    driver = ogr.GetDriverByName("ESRI Shapefile")
elif fileType == 'GDB':
    driver = ogr.GetDriverByName("FileGDB")
    
dirOutput = runSCSData['output']['output_ws']

dfLkpSoil = pd.read_csv(r'lookups\lkp_soil_V2.csv',index_col=0)
dfLkpLanduse = pd.read_csv(r'lookups\lkp_landuse_v1.csv',index_col=0,header=0)
dfLkpCN = pd.read_table(r'lookups\lkp_cn_v1.txt',index_col=0,sep='\t')
      
def calculate_cn(FAOSOIL,grid_code,SLOPEFRA):
    """
    @param FAOSOIL: I-Af-3c , Ge63-2/3a etc
    @param grid_code: 11,14,20
    @param SLOPEFRA: float 
    """
    
    CN = 0 # default value
    default_used = False
    message = None
    cn_key = ''
    soil_type = ''
    try:
        cover_type = dfLkpLanduse.ix[grid_code,'cover_type']
        cn_key = dfLkpLanduse.ix[grid_code,'Lkp_LU']
        
        if cover_type.lower() == 'row crops':
            #HC_text = dfLkpLanduse.ix[grid_code,'Lkp_LU']
            
            if SLOPEFRA<0.02:
                cn_key = 'Row Crops (SR), good'
            elif SLOPEFRA <0.08:
                cn_key = 'Row Crops (C), good'
            else:
                cn_key = 'Row Crops (C&T), good'
                        
        soil_type = dfLkpSoil.ix[FAOSOIL,'likely_HSG'][0][0]
        
        #print cn_key,soil_type
        
        CN = dfLkpCN.ix[cn_key,soil_type]
        
    except IndexError:
        default_used = True
        message = 'index error -[%s]' %grid_code
    except Exception, e:
        default_used = True
        message = e 
    finally:
        #return CN,default_used,message
        return CN,default_used,message,cn_key,soil_type
    

def calc_cn_from_landuse_intersected():
    """
    @summary: 
    @note:
              1. load catchment the shape file
              2. load soil_landuse_catch the shape file
              3. calculate the CN code
              4. calculate the aggregated CN for catchment
              5. update the catchment shapefile
    """
    
    dictCatchment = dict()
        
    workingFolder =  runSCSData['output']['output_ws']
    shpCatchment = runSCSData['input']['catchment_fn']
    csvCatchmentCN = runSCSData['output']['csvfn_catchment_cn']
    csvCatchmentSlope = runSCSData['output']['csvfn_catchment_slope']
    

    shpSoilLand = runSCSData['input']['catchment_landuse_fn']
    csvSoilLand=runSCSData['output']['csvfn_catchment_cn_landuse']
    
    ''' 1. load catchment slope csv file '''
    dfCatchmentSlope = pd.read_csv(csvCatchmentSlope,index_col=0,header=0)
    
    ''' 2. load soil_landuse_catch the shape file '''   
    print shpSoilLand
    ds = driver.Open(shpSoilLand, 0)
    vlayerSoilLand=ds.GetLayer(0)
    if ds is None:
        print 'Could not open file:' + shpSoilLand
        sys.exit(1)
                    
    ''' 3. calculate the CN code '''    
    lstSoilLand = []
    
    feat = vlayerSoilLand.GetNextFeature()
    while feat:    
        #=======================================================================
        # CN,default_used,message,cn_key,soil_type = calculate_cn(str(feat.GetField('FAOSOIL')),
        #                                        int(feat['grid_code'].toString()),
        #                                        dfCatchmentSlope.ix[int(feat['HydroID'].toString()),'SLOPEFRA'])            
        #=======================================================================
        
        CN,default_used,message,cn_key,soil_type = calculate_cn(str(feat.GetField('FAOSOIL')),
                                               int(feat.GetField('grid_code')),
                                               dfCatchmentSlope.ix[int(feat.GetField('HydroID')),'SLOPEFRA'])
        
        geom = feat.GetGeometryRef()
        area = geom.GetArea()
        if CN ==0:
            eff_area=0
        else:
            eff_area = area/10**6
        #print  CN,default_used,message
        
        lstSoilLand.append({'HydroID':str(feat.GetField('HydroID')),
                            'FAOSOIL':str(feat.GetField('FAOSOIL')),
                            'soil_type':soil_type,
                            'grid_code': int(feat.GetField('grid_code')),
                            'cn_key':cn_key ,           
                            'CN':CN,
                            'area':area/10**6,
                            'eff_area':eff_area,
                            'default_used':default_used,
                            'message':message})
        
        feat = vlayerSoilLand.GetNextFeature()
        
    ''' 4. calculate the aggregated CN for catchment '''
    dfCatchmentSoilLand = pd.DataFrame(lstSoilLand)    
    dfCatchmentSoilLand.index = dfCatchmentSoilLand['HydroID']
    dfCatchmentSoilLand['cn_area']=dfCatchmentSoilLand['CN'] * dfCatchmentSoilLand['area']
    
    dfCatchmentSoilLand.to_csv(csvSoilLand)
    
    
    dfSoilLand_groupbycatchment = dfCatchmentSoilLand.groupby(dfCatchmentSoilLand['HydroID'])    
    dfCatchmentCN = pd.DataFrame(dfSoilLand_groupbycatchment['cn_area'].sum()/dfSoilLand_groupbycatchment['eff_area'].sum(),columns = ['CN'])
    
    dfSoilLand_groupbyCN = dfCatchmentSoilLand.groupby(dfCatchmentSoilLand['CN'])
    dfSoilLand_groupbyCN['area'].sum().plot(kind='bar') 
    plt.title('Total area for each CN number (km2)')
    plt.savefig(runSCSData['output']['pngfn_CN_Area_summary'])
    
    ''' 5. Add default values '''
    dfCatchmentCN['CAREA']=0
    dfCatchmentCN['CAREA']=dfSoilLand_groupbycatchment['area'].sum()
    
    dfCatchmentCN['STDUR']=24
    dfCatchmentCN['ARF']=1
    dfCatchmentCN['DELTAT']=0.1
    dfCatchmentCN['STPROF']='SCSIa'
    dfCatchmentCN['ia']=0.2
    dfCatchmentCN['DELTAT']=0.1
    dfCatchmentCN['RETARD']=dfCatchmentCN['CN']
    dfCatchmentCN['DUHPRF']=484     
    dfCatchmentCN['BASEFLOW']=0
                  
    dfCatchmentCN.to_csv(csvCatchmentCN)
    

    print 'The END of calc_cn_from_landuse_intersected'
    
def prepare_cat_slope_flowLen_Outlet():
    
    
    fdbName = runSCSData['input']['input_ws']
    lyrnmCatchment = runSCSData['input']['catchment_name']                      #HydroID
    lyrnmLongestFlowPath  = runSCSData['input']['longest_flow_path_name']       #DrainID
    lyrnmDrainagePoints = runSCSData['input']['drainage_point_name']            #DrainID
    
    wsName =runSCSData['input']['input_ws']
    shpNmCatchment = runSCSData['input']['catchment_fn']                       #HydroID
    shpNmLongestFlowPath  = os.path.join (wsName,runSCSData['input']['longest_flow_path_name']+'.shp' )           #DrainID  
    shpNmDrainagePoints =os.path.join (wsName, runSCSData['input']['drainage_point_name']+'.shp'   )           #DrainID   #not used for adjoinCatchment  'DrainPointD3km1.shp' 


    """ catchment layer """
    
    if fileType == 'GDB':
        ds = driver.Open(fdbName, 0)
        lyrCatchment = ds.GetLayer(lyrnmCatchment)
    elif fileType=='SHP':       
        ds = driver.Open(shpNmCatchment, 0)
        lyrCatchment=ds.GetLayer(0)
        if ds is None:
            print 'Could not open file:' + shpNmCatchment
            sys.exit(1)
            
            
    lstCatchment = []
    feat = lyrCatchment.GetNextFeature()
    while feat:
        #print feat.GetField('HydroID'),feat.GetField('DrainID')
        
        lstCatchment.append({'HydroID':feat.GetField('HydroID'),                        
                            'area':feat.GetField('Shape_Area')})
        feat = lyrCatchment.GetNextFeature()
        
    dfCatchment = pd.DataFrame(lstCatchment)    
    dfCatchment.index = dfCatchment['HydroID']
    #print dfCatchment.to_string()
    
    
    """ average slope table """
    dfCatchment['SLOPEFRA']=0
    fo = open(runSCSData['output']['csvfn_catchment_slope'])
    for line in csv.DictReader(fo):
        dfCatchment.ix[int(line['HydroID']),'SLOPEFRA']=line['SLOPEFRA']
    
    """ longest flow path layer """    
    if fileType == 'GDB':
        lyrLongestFlowPath = ds.GetLayer(lyrnmLongestFlowPath)
    elif fileType=='SHP':       
        ds = driver.Open(shpNmLongestFlowPath, 0)
        if ds is None:
            print 'Could not open file:' + shpNmLongestFlowPath
            sys.exit(1)
        lyrLongestFlowPath = ds.GetLayer(0)    
    
    dfCatchment['LENGTH']=0
    
    feat = lyrLongestFlowPath.GetNextFeature()
    while feat:
        dfCatchment.ix[feat.GetField('DrainID'),'LENGTH']=feat.GetField('Shape_Leng')
        feat = lyrLongestFlowPath.GetNextFeature()
    
    """ drainage point layer """
    if fileType == 'GDB':
        lyrDrainagePoints = ds.GetLayer(lyrnmDrainagePoints)
    elif fileType=='SHP':       
        ds = driver.Open(shpNmDrainagePoints, 0)
        if ds is None:
            print 'Could not open file:' + shpNmDrainagePoints
            sys.exit(1)
        lyrDrainagePoints = ds.GetLayer(0)    
        
    dfCatchment['X']=0
    dfCatchment['Y']=0
        
    if not isAdj:      
        feat = lyrDrainagePoints.GetNextFeature()
        while feat:
            dfCatchment.ix[feat.GetField('DrainID'),'X']=feat.GetField('Easting')
            dfCatchment.ix[feat.GetField('DrainID'),'Y']=feat.GetField('Northing')
            feat = lyrDrainagePoints.GetNextFeature()
    else:
        # derive the drainage points from longest flow paths 
        if fileType == 'GDB':
            lyrLongestFlowPath = ds.GetLayer(lyrnmLongestFlowPath)
        elif fileType=='SHP':       
            ds = driver.Open(shpNmLongestFlowPath, 0)
            if ds is None:
                print 'Could not open file:' + shpNmLongestFlowPath
                sys.exit(1)
            lyrLongestFlowPath = ds.GetLayer(0)    
        
        #lyrLongestFlowPath.ResetReading()   # somehow it stops working
        feat = lyrLongestFlowPath.GetNextFeature()
        while feat:
            geom = feat.GetGeometryRef()
            #print geom.GetX(0),geom.GetY(0)
            pointsCount = geom.GetPointCount()
            dfCatchment.ix[feat.GetField('DrainID'),'X']=geom.GetX(pointsCount-1)
            dfCatchment.ix[feat.GetField('DrainID'),'Y']=geom.GetY(pointsCount-1)
            feat = lyrLongestFlowPath.GetNextFeature()        
    
    ''' CN numbers '''
    dfCatchmentCN = pd.read_csv(runSCSData['output']['csvfn_catchment_cn'],index_col=0,header=0)
    
    dfCatchmentFinal = pd.concat([dfCatchmentCN,dfCatchment],axis=1)
    dfCatchmentFinal.to_csv(runSCSData['output']['csvfn_catchment_processed'])            
    #print dfCatchmentFinal.to_string()
    
    
    print 'THE END of prepare_cat_slope_flowLen_Outlet'    
    
def derive_scs_model_using_rainfall():
    """
    @summary: 1) loop through rainfall event and combined with prepared catchment data to prepare SCS csv files
              2) call ISISHydrology.exe to calculate the flows
    
    """        
        
    dirOutputRoot = runSCSData['output']['output_scs_ws']
    rainDirCSV =  runSCSData['output']['output_rainfall_ws']
    
    dfCatchment = pd.read_csv(runSCSData['output']['csvfn_catchment_processed'],index_col=0,header=0)
    InFCName =runSCSData['input']['catchment_name']
    
    
    
    for k,dataConfig in rainData.items():
              
        rainfallZonalOutput = InFCName + '_' + dataConfig['oGrid']

        dirOutput = os.path.join(dirOutputRoot,dataConfig['oGrid'],InFCName)
        
        if not os.path.isdir(dirOutput):
            os.makedirs(dirOutput)

        csvFNOutput = os.path.join(dirOutput,rainfallZonalOutput + '.csv')
                    
        rainfallCSV =os.path.join(rainDirCSV, rainfallZonalOutput + '.csv' )
        dfRaifall = pd.read_csv(rainfallCSV,index_col=0,header=0)
        dfFinal = pd.concat([dfRaifall,dfCatchment],axis=1)
        dfFinal['Comment']=dataConfig['oGrid']
        dfFinal['STDUR']=24
        dfFinal.index.name = 'Label'
        #dfFinal['Label'] = dfRaifall['HydroID.1']
                        
        dfFinalCln = dfFinal[dfFinal['STDEPTH'].notnull()]
        dfFinalCln.to_csv(csvFNOutput)
        
        ''' 2. call ISISHydrology.exe'''

        cmd=[ExeISISHydrology,'-f'+csvFNOutput]
        print cmd
        proc = subprocess.Popen(cmd,shell=True)
        proc.wait()
        print proc.returncode        
    print 'END OF derive_scs_model_using_rainfall' 
    
if __name__ == '__main__':
    #calc_cn_from_landuse_intersected()
    #prepare_cat_slope_flowLen_Outlet()    
    
    
    derive_scs_model_using_rainfall()
