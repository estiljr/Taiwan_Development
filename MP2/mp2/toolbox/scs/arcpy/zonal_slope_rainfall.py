import arcpy
import os
from  collections import defaultdict
import pprint

from data_setup import *



def zonal_slope():
    '''
    @summary: 1. derive the zonal average from input detph slope grid for the input subcatchmetn layer
              2. export the results to a csv file for aggregation later
    '''
    
    arcpy.env.scratchWorkspace =runSCSData['input']['scratch_ws']
    arcpy.env.overwriteOutput = True     
    arcpy.env.workspace =runSCSData['input']['input_ws']
    
    #slope is in %age, scs requires fraction
    slope_grd = runSCSData['input']['slope_grd_name']
    OutTable= runSCSData['intermediate']['slope_zonal_table']
    OutCSV =runSCSData['output']['csvfn_catchment_slope']
    
    InFC = runSCSData['input']['catchment_fn']
           
        
    ''' 1. zonal analysis '''
    arcpy.CheckOutExtension("spatial")
    
    arcpy.sa.ZonalStatisticsAsTable(InFC, 'HydroID', slope_grd,  OutTable, 'DATA', 'ALL')
    print arcpy.GetMessages()
    arcpy.CheckInExtension("spatial")
    
    ''' 2. output as csv '''
    fo=open(OutCSV,'w')
    fo.write('HydroID,SLOPEFRA'+'\n')
    rows = arcpy.SearchCursor(OutTable, "", "", "HydroID; MEAN") 
    
    for row in rows: 
        #slope is in %age, scs requires fraction
        fo.write(','.join([str(row.HydroID),str(row.MEAN/100)])+'\n')

    print '-'*100
    print  'zonal slope - done'
    print '-'*100            

def zonal_rainfall():
    """
    @summary: 1. derive the zonal average from input rainfall grid for the input subcatchmetn layer
              2. export the results to a csv file for aggregation later
    @note:   the input rainfall grid is derived using method derive_rainfall_depth_grids()
    """
    
    #TODO: the output have different count of catchments from the input as some rainfall values aggregated to 0
    fileType = 'SHP'
    
    arcpy.env.scratchWorkspace =runSCSData['input']['scratch_ws']
    arcpy.env.overwriteOutput = True     
    arcpy.env.workspace =runSCSData['output']['output_rainfall_ws']
    outDirCSV=runSCSData['output']['output_rainfall_ws']
    
    InFCName =  runSCSData['input']['catchment_name']
    InFC= runSCSData['input']['catchment_fn']
        
    ''' 2. zonal rainfall depth'''    
    arcpy.CheckOutExtension("spatial")    

    for event, dataConfig in rainData.items():

        OutTable = InFCName + '_' + dataConfig['oGrid']
        rainGrid = dataConfig['oGrid']

        OutCSV =os.path.join(outDirCSV, OutTable + '.csv' )
        
        ''' a. zonal stats '''
        arcpy.sa.ZonalStatisticsAsTable(InFC, 'HydroID', rainGrid, 
                                        OutTable, 'DATA', 'ALL')    
        print arcpy.GetMessages()
        
        ''' b. output as csv'''
        fo=open(OutCSV,'w')
        fo.write('HydroID,STDEPTH'+'\n')
        rows = arcpy.SearchCursor(OutTable, "", "", "HydroID; MEAN") 
        
        for row in rows: 
            fo.write(','.join([str(row.HydroID),str(row.MEAN)])+'\n')
        
    arcpy.CheckInExtension("spatial")

    
    print '-'*100
    print  'zonal rainfall - done'
    print '-'*100
            
def derive_rainfall_depth_grids(Interp_type):
    '''
    @summary: a series of rainfall depth surface grids are derived using the various rainfall attributes in the input rain gauge shapefile
    @note:    rainfall gauges should be in TW97 CRS
    '''
             
    rainGaugeShp = runSCSData['input']['rain_gauge_fn']  # @UndefinedVariable
    rainOutDir = runSCSData['output']['output_rainfall_ws']
    
    if not os.path.isdir(rainOutDir):
        os.mkdir(rainOutDir)
    
    # different from the usual setup where input_ws is the workspace  
    arcpy.env.workspace = rainOutDir
            
    arcpy.env.scratchWorkspace =runSCSData['input']['scratch_ws']
    arcpy.env.overwriteOutput = True     
    arcpy.CheckOutExtension("spatial")

    extentLayer = arcpy.mapping.Layer(runSCSData['input']['catchment_fn'])
    arcpy.env.extent= extentLayer.getExtent()    
        
    for event, dataConfig in rainData.items():
        rainAttribute = dataConfig['FieldName']
        
        outputSize = 1000
        
        if Interp_type == 'IDW':
            outputGrid = dataConfig['oGrid']
            res = arcpy.sa.Idw(rainGaugeShp, 
                         rainAttribute,                      
                         outputSize, '2', 'VARIABLE 12','#')
        
        elif Interp_type =='KRIGING':
            outputGrid = dataConfig['oGrid']
            res = arcpy.sa.Kriging(rainGaugeShp, 
                                     rainAttribute,
                                     'LinearDrift', outputSize, 'VARIABLE 12', '#')
        res.save(outputGrid)            
        print arcpy.GetMessages()
    arcpy.CheckInExtension("spatial")
    
    print '-'*100
    print  'derive_rainfall_depth_grids - done'
    print '-'*100
    
def derive_rainfall_depth_grids_using_coKriging():
    """ !!!coKriging not working!!!!"""
    rainOutDir = r'C:\temp\taiwan\rainfall\rainfall_coKriging'
    
    if not os.path.isdir(rainOutDir):
        os.mkdir(rainOutDir)
    arcpy.env.workspace = rainOutDir
    arcpy.CheckOutExtension("GeoStats")
    
    inputGA ="Ordinary Cokriging"
    
    inputDset1 = r'C:\temp\taiwan\zonal\Raingauges_ALL-NORTH-ONLY3.shp' + " "+ 'ExistDepth' 
    inputDset2 = r'C:\temp\taiwan\rainfall\dtm\dtm_taipei.tif'
    VARCOVAR = inputDset1 + ";" + inputDset2
    
    #outLayer
    out = "cok"  
    outLayer = 'RP100N_KRG'
    
    arcpy.ga.GACreateGeostatisticalLayer(inputGA,VARCOVAR,outLayer)
    print arcpy.GetMessages()
   
if __name__=='__main__':

    derive_rainfall_depth_grids(Interp_type)
    
    zonal_rainfall()
    #zonal_slope()
    #pprint.pprint(runSCSData)