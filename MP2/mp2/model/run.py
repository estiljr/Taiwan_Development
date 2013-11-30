
import os
from collections import defaultdict


from  mp2.workflow.setup import configDict

class RunArchive(object):
    def __init__(self):
        self.version = None
        pass
    
class Run(object):

    #===========================================================================
    #TODO: .....
    # def __del__(self):
    #     QgsApplication.exitQgis()
    #===========================================================================
            
    def __init__(self, name, isInStore = True):
        """
        @summary: 
        @param isInStore: whether it is a run in model store or Running model
        @note: 
            1) set up all the run folder/files info
            2) read from db, 
            3) set the self._obj_domain is the domain object is available from outside.....
        """

        self._name = name  #Cat0001_Dom004_1000Yr_ND        
        self._domainName = name[:20]  #Cat0001_Dom004
        self._senarioSuffix = name[21:]  # 1000Yr_ND
               

        self._ModelFiles = defaultdict(dict)

        self._ISIS2D_to_ASC_path = configDict['exe']['isis2d_to_asc']

        self._ModelFiles['dir_domain'] = os.path.join(configDict['file_system']['model_store'], self._domainName)
        
        #E:\Models\RunningModels\Ha105_Cat2663_Dom015_100Yr_ND
        self._ModelFiles['dir_run_sim'] = os.path.join(configDict['file_system']['running_sim_dir'], self._name)
        
        if isInStore:
            self._ModelFiles['dir_run'] = os.path.join(self._ModelFiles['dir_domain'], self._name)
        else:
            #E:\Models\RunningModels\Ha105_Cat2663_Dom015_100Yr_ND\Model\Ha105_Cat2663_Dom015_100Yr_ND
            self._ModelFiles['dir_run'] = os.path.join(self._ModelFiles['dir_run_sim'], 'Model', self._name)

        
        self._dir_run = self._ModelFiles['dir_run']

        #self.__logger = logging.getLogger('mp2.run')
        
        #self.__read_run_from_db()
        self.__obj_domain = None

        self.__obj_mb = None
        self.__obj_log = None
        self.__geom_wkb_floodextent = None
    
    def establish_folder_structure (self):
        self._ModelFiles['folder_run_model_store'] = os.path.join(self._ModelFiles['dir_domain'], self._name)

        self._ModelFiles['dir_gis'] = os.path.join(self._ModelFiles['dir_run'], 'GIS')
        self._ModelFiles['dir_topo'] = os.path.join(self._ModelFiles['dir_gis'], 'topo')
        self._ModelFiles['dir_roughness'] = os.path.join(self._ModelFiles['dir_gis'], 'roughness')
        self._ModelFiles['dir_lateral_inflows'] = os.path.join(self._ModelFiles['dir_gis'], 'lateral_inflows')


        #self._ModelFiles['file_libray_IC'] = os.path.join(self._ModelFiles['dir_domain'], 'IC', self._name)
        #self._ModelFiles['dir_CHKPT'] = os.path.join(self._ModelFiles['dir_domain'], 'CHKPT', self._name)


        self._ModelFiles['dir_model_01'] = os.path.join(self._ModelFiles['dir_run'], 'model_01')

        self._ModelFiles['shp_active_area'] = os.path.join(self._ModelFiles['dir_gis'], 'Active_Area.shp')
        self._ModelFiles['shp_flow_lines'] = os.path.join(self._ModelFiles['dir_gis'], 'Flow_Lines.shp')
        self._ModelFiles['shp_z_polygons'] = os.path.join(self._ModelFiles['dir_gis'], 'Z_Polygons.shp')
        self._ModelFiles['shp_z_lines'] = os.path.join(self._ModelFiles['dir_gis'], 'Z_Lines.shp')

        self._ModelFiles['shp_roughness_mod'] = os.path.join(self._ModelFiles['dir_gis'], 'roughness_modifications.shp')

        self._ModelFiles['shp_flood_extent'] = os.path.join(self._ModelFiles['dir_model_01'],'flood_extent.shp')
        #self._ModelFiles['shp_flood_extent_single'] = os.path.join(self._ModelFiles['dir_model_01'],'flood_extent_singlePart.shp')
        
        
        self._ModelFiles['file_xml'] = os.path.join(self._ModelFiles['dir_run'], 'model.xml')
        self._ModelFiles['file_mb'] = os.path.join(self._ModelFiles['dir_run'], 'MB.csv')
        self._ModelFiles['file_model_log'] = os.path.join(self._ModelFiles['dir_run'], 'model.log')
        self._ModelFiles['file_slave_log'] = os.path.join(self._ModelFiles['dir_run'], 'slave.log')
        self._ModelFiles['file_iwl_in_model'] = os.path.join(self._ModelFiles['dir_run'], 'GIS', 'iwl.asc')
        self._ModelFiles['file_meta'] = os.path.join(self._ModelFiles['dir_run'], self._name + '.meta.csv')

        self._ModelFiles['file_2dm'] = os.path.join(self._ModelFiles['dir_model_01'], '01.2dm')
        self._ModelFiles['dat_water_level'] = os.path.join(self._ModelFiles['dir_model_01'], '01_waterlevel.dat')
        self._ModelFiles['dat_froud'] = os.path.join(self._ModelFiles['dir_model_01'], '01_froude_.dat')

        #asciiTime = self.getAsciiTime(self._ModelFiles['dir_run'])
        asciiTime = '3'
        if asciiTime is not None:
            self._ModelFiles['asc_depth'] = os.path.join(self._ModelFiles['dir_model_01'], '01_depth_' + asciiTime + '.asc')
            self._ModelFiles['asc_velocity'] = os.path.join(self._ModelFiles['dir_model_01'], '01_velocity_' + asciiTime + '.asc')
            self._ModelFiles['asc_froude'] = os.path.join(self._ModelFiles['dir_model_01'], '01_froude_' + asciiTime + '.asc')
            self._ModelFiles['asc_level'] = os.path.join(self._ModelFiles['dir_model_01'], '01_waterlevel_' + asciiTime + '.asc')

        self._ModelFiles['qgis_run'] = os.path.join(self._ModelFiles['dir_run'], 'scenario_project.qgs')
        self._ModelFiles['qgis_domain'] = os.path.join(self._ModelFiles['dir_domain'], 'domain_project.qgs')        
if __name__ == '__main__':
    pass