
from lxml import etree
import os

# bCElement.text = 'verticalflow'
# valueElement.set('type', 'timevar')
            
class ModelXML(object):
    def __init__(self,xml_name):
        self._xml_name = xml_name
        
        if os.path.isfile(self._xml_name):             
            xmlFile = open(xml_name, 'r')
            parser = etree.XMLParser(remove_blank_text = True) 
            self._tree = etree.parse(xmlFile, parser)  
            xmlFile.close()
            
            self._ISIS2D_NS = 'http://www.halcrow.com/ISIS2D'
            self._ISIS2D = '{%s}' % self._ISIS2D_NS
            self._NSMAP = {'i2d' : self._ISIS2D_NS}
        else:
            raise Exception('xml file do not exist : ' + self._xml_name)
        
    def get_total_hrs(self):
        return float(self._tree.find('i2d:domain/i2d:time/i2d:total', namespaces = self._NSMAP).text)

    def get_time_step(self):
        return float(self._tree.find('i2d:domain/i2d:run_data/i2d:time_step', namespaces = self._NSMAP).text)

    def get_scheme(self):
        return self._tree.find('i2d:domain/i2d:run_data/i2d:scheme', namespaces = self._NSMAP).text
      
    def get_fail_on_non_convergence(self):
        stop = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence', namespaces = self._NSMAP)
        attributes = stop.attrib
        flag = attributes['fail_on_non_convergence']
        if flag.lower() == 'true':
            return True
        else:
            return False
    
    def get_volume_comparison_percentage(self):
        ele = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:volume_comparison_percentage', namespaces = self._NSMAP)    
        if ele is not None:
            return float(ele.text)
        else:
            return 0
        
    def get_total_inflow_comparison_percentage(self):
        ele = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:total_inflow_comparison_percentage', namespaces = self._NSMAP)    
        if ele is not None:
            return float(ele.text)
        else:
            return 0
        
    def get_smallest_inflow_comparison_percentage(self):
        ele = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:smallest_inflow_comparison_percentage', namespaces = self._NSMAP)
        if ele is not None:
            return float(ele.text)
        else:
            return 0

    def get_minimum_run_time(self):
        return float(self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:minimum_run_time', namespaces = self._NSMAP).text)
 
    def get_flag_mass_error(self):
        
        ele = self._tree.find('i2d:advanced_options/i2d:flag_mass_error', namespaces = self._NSMAP)
        if ele is None:
            return 0,0
        else:
            attributes = ele.attrib
            #<!-- BEWARE: check_after_seconds is an INTEGER variable -->
            return int(attributes['check_after_seconds']), float(attributes['tolerance_pct'])

    def get_correct_negative_depths(self):
        if self._tree.find('i2d:advanced_options/i2d:correct_negative_depths', namespaces = self._NSMAP) is None:
            return False
        else:
            return True
    
    def print_run_settings(self):
        print 'scheme : %s' %self.get_scheme()
        print 'Time step : %s' %self.get_time_step()
        
        print 'total hrs: %s' %self.get_total_hrs()
        print 'min hrs : %s' %self.get_minimum_run_time()
        
#         print self.get_flag_mass_error()
#         print self.get_flag_mass_error()[1]

        print 'check MB after : %s' %self.get_flag_mass_error()[0]
        print 'failed with MB  : %s' %str(self.get_flag_mass_error()[1])        
        
        print 'fail on non_convergence: %s' %self.get_fail_on_non_convergence()
        print 'Convergence volumn : %s' %self.get_volume_comparison_percentage()
        print 'Convergence total inflow : %s' %self.get_total_inflow_comparison_percentage()
        print 'Convergence smallest inflow : %s' %self.get_smallest_inflow_comparison_percentage()
        
    def write_xml_file(self,fileName):    
        if os.path.isfile(fileName):
            os.remove(fileName)
        
        self._tree.write(fileName, pretty_print = True)   
                   
    def set_total_hrs(self,value, write_out=True, fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:domain/i2d:time/i2d:total', namespaces = self._NSMAP)    
        element.text = str(value)       
        if write_out == True: 
            self.write_xml_file(fileName)  

    def set_minimum_run_time(self,value, write_out=True,fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:minimum_run_time', namespaces = self._NSMAP)    
        element.text = str(value)        
        if write_out == True: 
            self.write_xml_file(fileName)  
                
    def set_time_step(self,value, write_out=True,fileName=None):
        if fileName is None:
            fileName = self._xml_name
            
        if value == 0:
            raise Exception('time step can not be set as 0')
        element = self._tree.find('i2d:domain/i2d:run_data/i2d:time_step', namespaces = self._NSMAP)    
        element.text = str(value)        
        if write_out == True: 
            self.write_xml_file(fileName)    
        
    def set_scheme(self,value,write_out=True, fileName=None):
        if fileName is None:
            fileName = self._xml_name
        
        #dealing with advanced correct negative depth
        if value == 'ADI':
            self.__set_correct_negative_depths(True, fileName)
        elif value == 'TVD':
            
            self.__set_correct_negative_depths(False, fileName)
        else:
            raise Exception('unrecognised scheme name :' + str(value))
        
        element = self._tree.find('i2d:domain/i2d:run_data/i2d:scheme', namespaces = self._NSMAP)    
        element.text = value.upper()        
        if write_out == True: 
            self.write_xml_file(fileName)      
        
    def set_fail_on_non_convergence(self,value,write_out=True, fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence', namespaces = self._NSMAP)
                 
        attributes = element.attrib
        attributes['fail_on_non_convergence'] = str(value).lower()
        if write_out == True: 
            self.write_xml_file(fileName)  
                    
    def set_volume_comparison_percentage(self,value, write_out=True,fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:volume_comparison_percentage', namespaces = self._NSMAP)    
        if value!=0:
            if element is None:
                #add one
                newElement = etree.Element(self._ISIS2D + 'volume_comparison_percentage', nsmap = self._NSMAP)  # @UndefinedVariable
                elementToInsertUnder = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence', namespaces = self._NSMAP)
                elementToInsertUnder.add(newElement)
                newElement.text = str(value)     
            else:
                element.text = str(value)                               
        else:
            if element is None:
                pass
            else:
                # delete it    
                element.getparent().remove(element) 
          
        if write_out == True: 
            self.write_xml_file(fileName)     
        
    def set_total_inflow_comparison_percentage(self,value, write_out=True,fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:total_inflow_comparison_percentage', namespaces = self._NSMAP)    
       
        if value!=0:
            if element is None:
                #add one
                newElement = etree.Element(self._ISIS2D + 'total_inflow_comparison_percentage', nsmap = self._NSMAP)  # @UndefinedVariable
                elementToInsertUnder = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence', namespaces = self._NSMAP)
                elementToInsertUnder.add(newElement)
                newElement.text = str(value)     
            else:
                element.text = str(value)                               
        else:
            if element is None:
                pass
            else:
                # delete it    
                element.getparent().remove(element) 
          
        if write_out == True: 
            self.write_xml_file(fileName)  
        
    def set_smallest_inflow_comparison_percentage(self,value,write_out=True, fileName=None):
        if fileName is None:
            fileName = self._xml_name
        element = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence/i2d:smallest_inflow_comparison_percentage', namespaces = self._NSMAP)    
        if value!=0:
            if element is None:
                #add one
                newElement = etree.Element(self._ISIS2D + 'smallest_inflow_comparison_percentage', nsmap = self._NSMAP)  # @UndefinedVariable
                elementToInsertUnder = self._tree.find('i2d:advanced_options/i2d:stop_on_convergence', namespaces = self._NSMAP)
                elementToInsertUnder.add(newElement)
                newElement.text = str(value)     
            else:
                element.text = str(value)                               
        else:
            if element is None:
                pass
            else:
                # delete it    
                element.getparent().remove(element) 
          
        if write_out == True: 
            self.write_xml_file(fileName)      
                         
    def set_flag_mass_error(self,check_after_seconds,tolerance_pct,write_out=True, fileName=None):
        if fileName is None:
            fileName = self._xml_name
        
        need_mb = True
        if check_after_seconds == 0 or tolerance_pct ==0 :
            need_mb = False
                    
        element = self._tree.find('i2d:advanced_options/i2d:flag_mass_error', namespaces = self._NSMAP)  
        
        if need_mb:
            if element is None:
                #add one
                mbElement = etree.Element(self._ISIS2D + 'flag_mass_error', nsmap = self._NSMAP)  # @UndefinedVariable
                elementToInsertAfter = self._tree.find('i2d:advanced_options/i2d:number_of_threads', namespaces = self._NSMAP)
                elementToInsertAfter.addnext(mbElement)
                mbElement.attrib['check_after_seconds'] = str(check_after_seconds)    
                mbElement.attrib['tolerance_pct'] = str(tolerance_pct)  
            else:
                element.attrib['check_after_seconds'] = str(check_after_seconds)    
                element.attrib['tolerance_pct'] = str(tolerance_pct)                                 
        else:
            if element is None:
                pass
            else:
                # delete it    
                element.getparent().remove(element) 
        if write_out == True: 
            self.write_xml_file(fileName)       
    
    def __set_correct_negative_depths(self,val,fileName=None):
        existEle= self._tree.find('i2d:advanced_options/i2d:correct_negative_depths', namespaces = self._NSMAP) 
        if existEle is None and val == False:
            pass
        elif existEle is not None and val == True:
            pass
        elif existEle is None and val == True:
            # creat a new one
            negElement = etree.Element(self._ISIS2D + 'correct_negative_depths', nsmap = self._NSMAP)  # @UndefinedVariable
            elementToInsertAfter = self._tree.find('i2d:advanced_options/i2d:number_of_threads', namespaces = self._NSMAP)
            elementToInsertAfter.addnext(negElement)
        elif existEle is not None and val == False:
            # delete one
            existEle.getparent().remove(existEle)


    
    
    