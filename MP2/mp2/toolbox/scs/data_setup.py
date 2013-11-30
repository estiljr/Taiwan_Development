from collections import defaultdict
import os

ExeISISHydrology = r'C:\temp\taiwan\scs\ISISHydrology\ISISHydrology.exe'

fileType = 'SHP' # 'GDB'
Interp_type = 'IDW' #'KRIGING'  'IDW'
rainData = defaultdict(dict)

if Interp_type == 'IDW':        
    rainData['RP2N']['RP'] = 2
    rainData['RP2N']['FieldName'] = 'NewD2' 
    rainData['RP2N']['oGrid'] =  'RP2N_IDW'
    
    rainData['RP2E']['RP'] = 2
    rainData['RP2E']['FieldName'] = 'ExistD2' 
    rainData['RP2E']['oGrid'] =  'RP2E_IDW'
     
    rainData['RP5N']['RP'] = 5
    rainData['RP5N']['FieldName'] = 'NewD5' 
    rainData['RP5N']['oGrid'] =  'RP5N_IDW'
     
    rainData['RP5E']['RP'] = 5
    rainData['RP5E']['FieldName'] = 'ExistD5' 
    rainData['RP5E']['oGrid'] =  'RP5E_IDW'
     
    rainData['RP100N']['RP'] = 100
    rainData['RP100N']['FieldName'] = 'NewD100' 
    rainData['RP100N']['oGrid'] =  'RP100N_IDW'
     
    rainData['RP100E']['RP'] = 100
    rainData['RP100E']['FieldName'] = 'ExistD100' 
    rainData['RP100E']['oGrid'] =  'RP100E_IDW'
         
    rainData['RP500N']['RP'] = 500
    rainData['RP500N']['FieldName'] = 'NewD500' 
    rainData['RP500N']['oGrid'] =  'RP500N_IDW'
     
    rainData['RP500E']['RP'] = 500
    rainData['RP500E']['FieldName'] = 'ExistD500' 
    rainData['RP500E']['oGrid'] =  'RP500E_IDW'
    
    
elif Interp_type =='KRIGING':
    rainData['RP2N']['RP'] = 2
    rainData['RP2N']['FieldName'] = 'NewD2' 
    rainData['RP2N']['oGrid'] =  'RP2N_KRG'
    
    rainData['RP2E']['RP'] = 2
    rainData['RP2E']['FieldName'] = 'ExistD2' 
    rainData['RP2E']['oGrid'] =  'RP2E_KRG'
     
    rainData['RP5N']['RP'] = 5
    rainData['RP5N']['FieldName'] = 'NewD5' 
    rainData['RP5N']['oGrid'] =  'RP5N_KRG'
     
    rainData['RP5E']['RP'] = 5
    rainData['RP5E']['FieldName'] = 'ExistD5' 
    rainData['RP5E']['oGrid'] =  'RP5E_KRG'
     
    rainData['RP100N']['RP'] = 100
    rainData['RP100N']['FieldName'] = 'NewD100' 
    rainData['RP100N']['oGrid'] =  'RP100N_KRG'
     
    rainData['RP100E']['RP'] = 100
    rainData['RP100E']['FieldName'] = 'ExistD100' 
    rainData['RP100E']['oGrid'] =  'RP100E_KRG'
         
    rainData['RP500N']['RP'] = 500
    rainData['RP500N']['FieldName'] = 'NewD500' 
    rainData['RP500N']['oGrid'] =  'RP500N_KRG'
     
    rainData['RP500E']['RP'] = 500
    rainData['RP500E']['FieldName'] = 'ExistD500' 
    rainData['RP500E']['oGrid'] =  'RP500E_KRG'
        
runSCSData = defaultdict(dict)

runSCSData['input']['input_ws']=r'C:\temp\taiwan\111\catchments'
runSCSData['input']['scratch_ws']=r"c:\temp\scratch"

runSCSData['input']['catchment_name']='adjcatchd3km1' #'catchd3km1'
runSCSData['input']['catchment_fn']=os.path.join(runSCSData['input']['input_ws'],runSCSData['input']['catchment_name']+'.shp')

runSCSData['input']['longest_flow_path_name']='LFPCatD3km1'  
runSCSData['input']['drainage_point_name']='DrainPointD3km1'
runSCSData['input']['catchment_landuse_fn']=os.path.join(runSCSData['input']['input_ws'],'soil_landuse_catchd3km1.shp')
needDrainagePoints = False #adj derives the drainage points from longest flow pathes

runSCSData['input']['slope_grd_name']='slope_per'
#runSCSData['input']['slope_grd_fn']=os.path.join(runSCSData['input']['input_ws'],runSCSData['input']['slope_grd_name'])

runSCSData['input']['rain_gauge_fn']=r'C:\temp\taiwan\111\rainfall\Raingauges_ALL-NORTH-ONLY5_TWD97_prj.shp'

runSCSData['intermediate']['slope_zonal_table']=runSCSData['input']['catchment_name']+'_slope'

runSCSData['output']['output_ws'] = r'C:\temp\taiwan\111\scs'
runSCSData['output']['output_rainfall_ws']= r'C:\temp\taiwan\111\rainfall'
runSCSData['output']['output_scs_ws']= r'C:\temp\taiwan\111\scs\scs_models'
runSCSData['output']['csvfn_catchment_slope']=os.path.join(runSCSData['output']['output_ws'],runSCSData['intermediate']['slope_zonal_table']+'.csv')
runSCSData['output']['csvfn_catchment_processed'] =os.path.join(runSCSData['output']['output_ws'], runSCSData['input']['catchment_name']+'_all_processed.csv' )
runSCSData['output']['csvfn_catchment_cn'] =os.path.join(runSCSData['output']['output_ws'], runSCSData['input']['catchment_name']+'_CN.csv' )
runSCSData['output']['csvfn_catchment_cn_landuse'] =os.path.join(runSCSData['output']['output_ws'], runSCSData['input']['catchment_name']+'_CN_soil_landuse.csv' )

runSCSData['output']['pngfn_CN_Area_summary'] = os.path.join(runSCSData['output']['output_ws'], runSCSData['input']['catchment_name']+'_CN_Area_summary.png' )
