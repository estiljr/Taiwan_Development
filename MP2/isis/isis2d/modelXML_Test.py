
import unittest
from isis.modelXML import ModelXML


class ModelXMLTest(unittest.TestCase):


    def test_get_total_hrs(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_total_hrs()
        self.assertEquals(100, value)

    def test_get_time_step(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_time_step()
        self.assertEquals(5.0, value)

    def test_get_scheme(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_scheme()
        self.assertEquals('ADI', value)        

    def test_get_stop_on_convergence(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_fail_on_non_convergence()
        self.assertEquals(True, value)
 
    def test_get_volume_comparison_percentage(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_volume_comparison_percentage()
        self.assertEquals(1, value)
 
    def test_get_total_inflow_comparison_percentage(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_total_inflow_comparison_percentage()
        self.assertEquals(1, value)      
        
    def test_get_smallest_inflow_comparison_percentage(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_smallest_inflow_comparison_percentage()
        self.assertEquals(67, value)
 
    def test_get_minimum_run_time(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_minimum_run_time()
        self.assertEquals(3, value)      
        
    def test_get_flag_mass_error(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_flag_mass_error()
        self.assertEquals(14400, value[0])
        self.assertEquals(50000, value[1])
 
    def test_get_correct_negative_depths(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        value = objXML.get_correct_negative_depths()
        self.assertEquals(True, value)             
        
    def test_set_total_hrs(self):
        #print 'test_set_total_hrs'
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_total_hrs(55,True,'test_files\Ha001_Cat0001_Dom010_new.xml')
         
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_new.xml')
        value = objXML2.get_total_hrs()
        self.assertEquals(55, value)                
    
    def test_set_minimum_run_time(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_minimum_run_time(57,True,'test_files\Ha001_Cat0001_Dom010_new.xml')
         
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_new.xml')
        value = objXML2.get_minimum_run_time()
        self.assertEquals(57, value)    
                    
    def test_set_time_step(self):
        #print 'test_set_time_step'
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_time_step(1,True,'test_files\Ha001_Cat0001_Dom010_new.xml')
        
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_new.xml')
        value = objXML2.get_time_step()
        self.assertEquals(1, value)   

    def test_set_scheme_adi_2_tvd(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_adi_2_tvd.xml'
        
        objXML = ModelXML(oldXML)
        objXML.set_scheme('TVD',True,newXML)
        
        objXML2= ModelXML(newXML)
        value1 = objXML2.get_scheme()
        value2 = objXML2.get_correct_negative_depths()
        self.assertEquals('TVD', value1)    
        self.assertEquals(False, value2)   

    def test_set_scheme_tvd_2_adi(self):

        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010_TVD.xml')
        objXML.set_scheme('ADI','test_files\Ha001_Cat0001_Dom010_tvd_2_adi.xml')
        
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_tvd_2_adi.xml')
        value1 = objXML2.get_scheme()
        value2 = objXML2.get_correct_negative_depths()
        self.assertEquals('ADI', value1)    
        self.assertEquals(True, value2)   

    def test_set_stop_on_convergence(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_fail_on_non_convergence(False,'test_files\Ha001_Cat0001_Dom010_new1.xml')
        
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_new1.xml')
        value = objXML2.get_fail_on_non_convergence()
        self.assertEquals(False, value)      
                
    def test_set_volume_comparison_percentage(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_new.xml'
        
        objXML = ModelXML(oldXML)
        objXML.set_volume_comparison_percentage(11,True,newXML)
        
        objXML2= ModelXML(newXML)
        value = objXML2.get_volume_comparison_percentage()
        self.assertEquals(11, value)                  

    def test_set_volume_comparison_percentage_to_none(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_volume_comparison_percentage(0,'test_files\Ha001_Cat0001_Dom010_none2.xml')
        
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_none2.xml')
        value = objXML2.get_volume_comparison_percentage()
        self.assertEquals(0, value)        
        
    def test_set_total_inflow_comparison_percentage(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_new.xml'
        
        objXML = ModelXML(oldXML)
        objXML.set_total_inflow_comparison_percentage(22,True,newXML)
        
        
        objXML2= ModelXML(newXML)
        value = objXML2.get_total_inflow_comparison_percentage()
        self.assertEquals(22, value)     

    def test_set_total_inflow_comparison_percentage_to_none(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_none.xml'
        
        objXML = ModelXML(oldXML)
        objXML.set_total_inflow_comparison_percentage(0,True,newXML)
        
        objXML2= ModelXML(newXML)
        value = objXML2.get_total_inflow_comparison_percentage()
        self.assertEquals(0, value)     
        
    def test_set_inflow_comparison_percentage(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_new.xml'
               
        objXML = ModelXML(oldXML)
        objXML.set_smallest_inflow_comparison_percentage(33,True,newXML)
        
        objXML2= ModelXML(newXML)
        value = objXML2.get_smallest_inflow_comparison_percentage()
        self.assertEquals(33, value)       
    
    def test_set_flag_mass_error(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
        newXML = 'test_files\Ha001_Cat0001_Dom010_new.xml'
               
        objXML = ModelXML(oldXML)
        objXML.set_flag_mass_error(1111, 2222,True,newXML)
        
        objXML2= ModelXML(newXML)
        value1, value2 = objXML2.get_flag_mass_error()
        self.assertEquals(1111, value1)      
        self.assertEquals(2222, value2)         

    def test_set_flag_mass_error_from_none(self):
        oldXML = 'test_files\Ha001_Cat0001_Dom010_noMB.xml'
        newXML ='test_files\Ha001_Cat0001_Dom010_withMB.xml'
        objXML = ModelXML(oldXML)
        
        objXML.set_flag_mass_error(1111, 2222,True,newXML)
        
        objXML2= ModelXML(newXML)
        value1, value2 = objXML2.get_flag_mass_error()
        self.assertEquals(1111, value1)      
        self.assertEquals(2222, value2)    

    def test_set_flag_mass_error_to_none(self):
        objXML = ModelXML('test_files\Ha001_Cat0001_Dom010.xml')
        objXML.set_flag_mass_error(0, 2222,True,'test_files\Ha001_Cat0001_Dom010_2NoMB.xml')
        
        objXML2= ModelXML('test_files\Ha001_Cat0001_Dom010_2NoMB.xml')
        value1, value2 = objXML2.get_flag_mass_error()
        self.assertEquals(0, value1)      
        self.assertEquals(0, value2)   
    
    #  set_correct_negative_depths is a private method    
    #===========================================================================
    # def test_set_correct_negative_depths(self):
    #     oldXML = 'test_files\Ha001_Cat0001_Dom010.xml'
    #     newXML = 'test_files\Ha001_Cat0001_Dom010_new.xml'
    #     
    #     objXML = ModelXML(oldXML)
    #     objXML.set_correct_negative_depths(True,True,newXML)
    #     
    #     objXML2= ModelXML(newXML)
    #     value = objXML2.get_correct_negative_depths()
    #     self.assertEquals(True, value)      
    #===========================================================================
 
                                     
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
