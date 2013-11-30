
import os
import csv
import sys
import math
from collections import defaultdict
import pprint
try:
    from osgeo import ogr
except:
    import ogr

from sqlalchemy.orm import sessionmaker,mapper
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData

from geoalchemy2 import Geometry

class RiverSection(object):
    '''
    @summary:  river cross section and could be prepared into ISIS format
    '''

    def __init__(self,label):
        self._river_section_name = label #251000_009, 1510A0_001.A ,114011_001.01
        
        self._river_name = self._river_section_name.split('_')[0] #251000
        self._section_name = self._river_section_name.split('_')[1] #009, _001.A
        
        try:
            # section name identification error
            self._section_number = float(self._section_name.split('.')[0])
            self._auto_order = 1
        except:
            self._section_number = 0 
            self._auto_order = 0
        
        ''' work out the node lable for section in ISIS'''
        self._node_lable = self._river_section_name[:12]
        if len(self._river_section_name)>12:
            self._label_shorten = 1
        else:
            self._label_shorten = 0
        #=======================================================================
        # if len(self._river_section_name) < 12 :
        #     self._node_lable = 'N' + self._river_section_name #N251000_009
        # else:            
        #     #name 251000_000.01 as 251000_000A
        #     try:
        #         left=self._river_section_name.split('.')[0]
        #         residual = self._river_section_name.split('.')[1]
        #         if residual.isdigit():
        #             right = chr(int(residual)+96)
        #         else:
        #             right = residual
        #         self._node_lable = ('N'+left+right)[:12]
        #     except Exception,e:
        #         print e
        #         print self._river_section_name
        #=======================================================================
        
        # section points might include the left and right banks as they are read in separately        
        self._section_points = []   #list of SectionPoint
        
        # left and right bank is identified using note column from survey data and x column
        self._left_bank = None      #SectionPoint
        self._right_bank = None     #SectionPoint
        
        # bed is determined by elevation
        self._bed = None            #SectionPoint
        
        self._next_section = None   #RiverSection
        self.__dist_to_next = None
        
        self._survey_year = None
        
        self._no_of_points = 0                
        self._section_number_derived = None  # what is this used for?
        
        self._auto_note = ''
        self.__accuracy = None #'a set of 's1' or 's2' depending on the number of decimal places for the survey points


    def __str__(self):
        return self._river_section_name

    def __repr__(self):
        return '<river section: %s, next section: %s, riverbed: %s>' %(self._river_section_name,str(self._next_section),str(self._bed))
                    
    def get_dist_to_next(self):
        if self.__dist_to_next is None:
            try:
                if self._next_section is None:
                    self.__dist_to_next = 0
                else:
                    self.__dist_to_next=self._bed.get_distance_from(self._next_section._bed)
            except:
                self.__dist_to_next = 999
        return self.__dist_to_next
                 
    def get_dat_format(self):
        """
        @summary: return the isis dat or ied format
        """
        #TODO: add special markers here
        #TODO: waht is the 0.0001 and 1000 here?
        
        #===============================================================================
        # RIVER this section
        # SECTION
        # dffd
        #    100.000              0.0001      1000
        #        253
        #    -18.490     2.740     0.040     1.000           292814.072783787.99          
        #    -14.110     2.550     0.040*    0.000LEFT       292816.592783791.57LEFT    
        #===============================================================================
        

        sOut = 'RIVER  ' + self._river_section_name +' survey year:' + str(self._survey_year) +  '\n'
        sOut += 'SECTION' + '\n'
        sOut += self._node_lable + '\n'
        sOut += str(round(self._dist_to_next,2)).rjust(10) + ' '*10 + format(0.001,'10.5') +  '1000'.rjust(10) + '\n'
        sOut += str(self._no_of_points).rjust(10) + '\n'
        
        for objSectionPoint in self._section_points:
            sOut += objSectionPoint.get_dat_format()
        return sOut
    
    
    def derive_bank_bed(self):
        """
        @summary: loop through the Section Points list to identify left/right bank and bed
        """
        
        ''' derive the Left bank (refenece point) if it is not tagged in original data '''
        left_bank_order = 0
        left_bank_found = False
        if self._left_bank._x is None:
            self._left_bank._x = 0 
        
            for i, objSectPnt in enumerate(self._section_points):
                if objSectPnt._x == 0:
                    objSectPnt._note = 'L_derived'
                    #left_bank_order = objSectPnt._order
                    left_bank_found = True
                    break
        else:
            left_bank_found = True
        
        if not left_bank_found:
            self._auto_note += 'survey reference point not found;'
        
            
        #=======================================================================
        # ''' derive the Right bank if it is not tagged in original data '''
        # if self._right_bank._x is None:
        #     self._section_points[-1]._note='R_derived'   
        #=======================================================================
                
        ''' find the bed as the lowest point'''
        #=======================================================================
        # for bed in sorted(self._section_points, key=lambda pnt : pnt._y):
        #     if bed._order > left_bank_order:
        #         bed._note = 'B_derived'
        #         self._bed = bed     
        #         bed._marker = 'BED'
        #         break
        #     else:
        #         self._auto_note += 'river bed not identified'
        #=======================================================================
        bed = sorted(self._section_points, key=lambda pnt : pnt._y)[0]
        self._bed = bed
        bed._marker = 'BED'
        bed_order = bed._order 
        
        ''' identify the left and right bank for ISIS'''
        #print self._river_section_name,len(self._section_points),bed_order
        try:
            leftBank = sorted(self._section_points[:bed_order], key=lambda pnt : pnt._y)[-1]
            leftBank._marker = 'LEFT'
            
            rightBank = sorted(self._section_points[bed_order:], key=lambda pnt : pnt._y)[-1]
            rightBank._marker = 'RIGHT'      
        except:
            self._auto_note += 'unable to identify left and/or right bank;'
                     
        self._no_of_points = len(self._section_points)


    def get_accuracy(self):
        if self.__accuracy is None:
            accuracy_set = set()
            for pnt in self._section_points:
                accuracy_set.add(pnt._gcp_type)
            if 's1' in accuracy_set:
                self.__accuracy ='s1'
            else:
                self.__accuracy = 's2'
        return self.__accuracy

    _accuracy = property(get_accuracy, None, None, None)        
    _dist_to_next = property(get_dist_to_next, None, None, None)


class SectionPoint(object):     
    """
    @summary: class represenation of survey points which make up the x-section
    @note:
              1) could return ISIS format using get_dat_format()
              2) could return x, y and using get_point_xy_format()
    """ 
    
    def __init__(self):
        self._gid = None
        self._note = ''         # supplied by TW WRA
        
        self._x =None           #  x, y is relative to the left bank
        self._y = None

        self._roughness = 0.035
        
        self.__easting = None    #  Easting and northing different from x and y
        self.__northing = None
        self.__tangent = None
        
        self._XSection = None       # RiverSection
        
        self.__marker = None        # used in ISIS
        self.__deactivation = None  # used in ISIS, closly linked with MARKER
        
        self._order = None          # order of points within section relative to the left bank
        self._name = None           # name is determined by section_name + order number
        self._gcp_type  = None      # s0 - bank marker; s1 - elevation as decimal digits; s2 - elevation as whole number
                    
    def __str__(self):
        return  '<%s : E: %s N: %s >' %(self._name,self._easting,self._northing)
    
    def __repr__(self):
        return '<Section point: %s>' %self._name
    
    def get_marker(self):
        #=======================================================================
        # if self.__marker is None:
        #     if self._note is not None and self._note != '':
        #         #print type(self._note)
        #         if self._note[0]=='L':
        #             self.__marker = 'LEFT'
        #         elif  self._note[0]=='R':
        #             self.__marker = 'RIGHT'
        #         elif self._note[0]=='B':
        #             self.__marker = 'BED'
        #=======================================================================
        return self.__marker


    def get_deactivation(self):
        if self.__deactivation is None:
            if self._marker == 'LEFT':
                self.__deactivation = 'LEFT'
            elif self._marker == 'RIGHT':
                self.__deactivation = 'RIGHT'
        return self.__deactivation


    def set_marker(self, value):
        self.__marker = value


    def set_deactivation(self, value):
        self.__deactivation = value

        
    def get_easting(self):
        ''' easting and northing is worked out via relative horizontal position against the left and right bank'''
        if self.__easting is None:
            if self._XSection._left_bank._easting < self._XSection._right_bank._easting:
                sign = 1
            else:
                sign = -1                
            self.__easting=self._XSection._left_bank._easting+sign*(self._x - self._XSection._left_bank._x )*math.sqrt(1/(1+self._tangent**2))
        return self.__easting


    def get_northing(self):
        if self.__northing is None:
            if self._XSection._left_bank._northing < self._XSection._right_bank._northing:
                sign = 1
            else:
                sign = -1
                
            self.__northing=self._XSection._left_bank._northing+sign*(self._x - self._XSection._left_bank._x )/math.sqrt(1+1/self._tangent**2)
        return self.__northing
    
    def get_tangent(self):
        if self.__tangent is None:
            self.__tangent = (self._XSection._left_bank._northing - self._XSection._right_bank._northing)/ \
                             (self._XSection._left_bank._easting - self._XSection._right_bank._easting)   
        return self.__tangent
                                
    def set_easting(self, value):
        self.__easting = value

    def set_northing(self, value):
        self.__northing = value

           
    _easting = property(get_easting, set_easting, None, None)
    _northing = property(get_northing, set_northing, None, None)   
    _tangent = property(get_tangent, None, None, None)  
    _marker = property(get_marker, set_marker, None, None)
    _deactivation = property(get_deactivation, set_deactivation, None, None)
        
       
    def get_dat_format(self):
        '''
        @return:  a string that in ISIS cross-section data format
                   -14.110     2.550     0.040*    0.000LEFT       292816.592783791.57LEFT   
        '''
  
        FIX_WIDETH=10
        sOut = format(self._x, '10.3f') 
        sOut += format(self._y, '10.3f')
        sOut += format(self._roughness, '10.3f')
        sOut += format(0, '10.3f') 
        if self._marker is not None:
            sOut += self._marker.ljust(FIX_WIDETH)
        else:
            sOut += ' '*10
        sOut += format(self._easting, '10.2f')
        sOut += format(self._northing, '10.2f')
        if self._deactivation is not None:
            sOut += self._deactivation.ljust(FIX_WIDETH)
        return sOut + '\n'
    
    def print_easting_northing(self):
        print format(self._easting, '10.2f') + ',' + format(self._northing, '10.2f')
    
    def get_point_xy_format(self):
        #return self._XSection._river_section_name + ',' + format(self._easting, '10.2f') + ',' + format(self._northing, '10.2f')+ ',' + format(self._y, '7.3f') + '\n'
        return ','.join([self._name, 
                         format(self._easting, '10.2f'),
                         format(self._northing, '10.2f'), 
                         format(self._y, '7.3f'),
                         str(self._gcp_type) + '\n'])
    
    def get_distance_from(self,otherPoint):
        return math.sqrt((self._easting-otherPoint._easting)**2 + (self._northing-otherPoint._northing)**2)

class RiverSectionDB(RiverSection):
    """
    @note: outdated now? prefer using orm
    """
    def __init__(self,dbConn):
        RiverSection.__init__(self)
        self._dbConn = dbConn
    
    def insert(self):
        qDict = dict()
        qDict['the_geom'] = self._the_geom
        
        qDict['river_name'] = self._river_name #251000
        qDict['section_name'] = self._section_name  #022
        qDict['river_section_name'] = self._river_section_name #251000_022
        
        qDict['left_bank_id'] = self._left_bank_id
        qDict['right_bank_id'] = self._right_bank_id
        qDict['bed_id'] = self._bed_id
        
        qDict['lb_easting'] = self._left_bank._easting
        qDict['lb_northing'] = self._left_bank._northing
        qDict['lb_z'] = self._left_bank._y
        
        qDict['rb_easting'] = self._right_bank._easting
        qDict['rb_northing'] = self._right_bank._northing
        qDict['rb_z'] = self._right_bank._y
        
        qDict['survey_year'] = self._survey_year
        qDict['next_section_id'] = self._next_section_id
        qDict['dist_to_next'] = self._dist_to_next
        
        qDict['no_of_points'] = self._no_of_points

        
        cur = self._dbConn.cursor()
        cur.execute("""INSERT INTO bg_gi.river_section(
            the_geom,             
            river_name, section_name, river_section_name,             
            left_bank_id, right_bank_id, bed_id,             
            lb_easting, lb_northing, lb_z, 
            rb_easting, rb_northing, rb_z, 
            survey_year, 
            next_section_id, dist_to_next)
            
            VALUES (%(the_geom)s, 
                    %(river_name)s, %(section_name)s, %(river_section_name)s, 
                    %(left_bank_id)s, %(right_bank_id)s, %(bed_id)s, 
                    %(lb_easting)s,%(lb_northing)s, %(lb_z)s, 
                    %(rb_easting)s, %(rb_northing)s, %(rb_z)s,
                    %(survey_year)s, 
                    %(next_section_id)s, %(dist_to_next)s 
                    );""",qDict)
        self._dbConn.commit()
    
    def read(self):
        pass

#===============================================================================
# engine = create_engine('postgresql://taiwan_user:taiwan@UKSD2F0W3J:5432/taiwan', echo=True)  
# metadata = MetaData()
# 
# section_point_table = Table('section_point', metadata,
#                 Column('id', Integer, primary_key=True),
#                 Column('geom',Geometry('POINT')),
#                 Column('name',String),
#                 Column('easting',Float),
#                 Column('northing',Float),
#                 Column('x',Float),
#                 Column('y',Float),
#                 Column('note',String),schema='bg_gi')
# 
# 
# mapper(SectionPoint,  section_point_table,  
#                     properties={ '_id':  section_point_table.c.id,
#                                  '_geom' : section_point_table.c.geom,
#                                 '_name':  section_point_table.c.name,
#                                 '_easting': section_point_table.c.easting,
#                                 '_northing':section_point_table.c.northing,
#                                 '_x': section_point_table.c.x,
#                                 '_y':section_point_table.c.y,
#                                 '_note':section_point_table.c.note,
#                                 })        
# 
# metadata.create_all(engine)
#===============================================================================

def read_survey_point_file(infile,type='ied',river='all'):    
    """
    @summary: the routine reads in the raw survey data provided by WRA and create section/survey points shp and IED files
    @param type:
                ied - output the ied format (each river a separate file)
                pnt - output a text file with (section_name , easting, northing and elevation) of the survey points (single file)
                shp - output a shape file with all x-sections
                shpbank - output the left/right bank marker 
    @param river:
                all - all survey sections are processed
                xxx - only section fit the pattern will be processed
    @note: 
    1) read in the file to produce xSections - a list of RiverSection objects
    2) finalise the xSections in terms of derivation of nextSection, dist_to_next, and left, right bank derivation 
    """
    
    #TODO: a new loop to look at each individual river and sort the secitons according to the numbers and 
    #write out the the lines on the database. results exported as per river names
    
    if not os.path.isfile(infile):
        print '[%s] does not exist' %infile 
        return
    
    with open(infile, 'rb') as f:
        reader = csv.DictReader(f)  
        rowNo = 0
        preSectionLabel = None

        
        # a dictionary with key being the river name and value a list of sections
        riverDict = defaultdict(list) 
        
        point_index_within_section = 1
        
        try:
            for row in reader:
                #print 'row number:' + str(rowNo)
                if river == 'all':
                    pass
                elif river not in str(row['ID']):
                    continue
                else:
                    pass
                    
#                 if str(row['ID']) =='163020_001':
#                     pass
                
                if str(row['ID']) != preSectionLabel:
                    ''' A new section starts '''
                                        
                    try:
                        
                        ''' Read in the *cross section* NOT *survey points* - label, left, right banks'''
                        
                        preSectionLabel= str(row['ID'])
                        objXSection = RiverSection(preSectionLabel)
                        
                        point_index_within_section = 1
                    
                        objXSection._left_bank = SectionPoint()
                        objXSection._left_bank._easting = float(row['Left_bank_TM97_X'])
                        objXSection._left_bank._northing = float(row['Left_bank_TM97_Y'])
                        try:
                            objXSection._left_bank._y = float(row['left_bank_elevation'])
                        except:
                            pass
                        
                        objXSection._left_bank._name = objXSection._river_section_name + '_L'
                        objXSection._left_bank._note = 'L'
                        objXSection._left_bank._gcp_type = 's0'
                        
#                         print 'left bank'
#                         objXSection._left_bank.print_easting_northing()
                        
                        # skip the right bank if info is missing or has error
                        try:
                            objXSection._right_bank = SectionPoint()
                            objXSection._right_bank._easting = float(row['Right_bank_TM97_X'])
                            objXSection._right_bank._northing = float(row['Right_bank_TM97_Y'])
                            objXSection._right_bank._y = float(row['right_bank_elevation'])
                            objXSection._right_bank._name = objXSection._river_section_name + '_R'
                            objXSection._right_bank._note = 'R'
                            objXSection._right_bank._gcp_type = 's0'
                        except:
                            pass
                        
                        objXSection._survey_year = int(row['Year'])
#                         print 'right bank'
#                         objXSection._right_bank.print_easting_northing()
                                      
                        riverDict[objXSection._river_name].append(objXSection)
                    except Exception,e:
                        print 'error happened when trying processing the left and right banks for the section'
                        print e
                        pprint.pprint(row)    
                                    
                try:
                    ''' read in every survey points'''        
                    objSectionPoint = SectionPoint()
                    objSectionPoint._XSection = objXSection
                    objSectionPoint._order = point_index_within_section
                    objSectionPoint._name = objSectionPoint._XSection._river_section_name +'_' +str(point_index_within_section)
     
                    objSectionPoint._x = float(row['cross_section_horizontal_distance'])
                    objSectionPoint._y = float(row['Elevation'])
                    
                    objSectionPoint._note = row['Note']
                    if objSectionPoint._y == int(objSectionPoint._y):
                        objSectionPoint._gcp_type = 's2'
                    else:
                        objSectionPoint._gcp_type = 's1'
                    
                    if 'L' in objSectionPoint._note:
                        objXSection._left_bank._x = float(row['cross_section_horizontal_distance'])
                    elif 'R' in objSectionPoint._note:
                        objXSection._right_bank._x = float(row['cross_section_horizontal_distance'])                
                    
                    objXSection._section_points.append(objSectionPoint)
                    
                    rowNo +=1
                    point_index_within_section +=1
                    
                except Exception,e:
                    print 'error happened when trying processing the survey points'
                    print e          
                    pprint.pprint(row)      
                

        except csv.Error, e: 
            sys.exit('file %s, line %d: %s' % (infile, reader.line_num, e))

        '''  generate the xSections to ied or csv'''
        if type == 'pnt':
            outfile = os.path.join(os.path.split(infile)[0], os.path.split(infile)[1].replace('.csv','.txt'))    
            fo = open(outfile,'w')
            fo.write('section_name,easting,northing,elevation,gcp_type\n')
        elif type == 'shp':
            
            ''' create shape file'''
            driver = ogr.GetDriverByName('ESRI Shapefile')
            
            inFileStub = os.path.split(infile)[1].split('.')[0]
            #inFileStub = 'x-section'
            shpName = inFileStub+'.shp'
            print shpName
            if os.path.exists(shpName):
                driver.DeleteDataSource(shpName) 
            ds2 = driver.CreateDataSource(shpName)
            
            spatialReference = ogr.osr.SpatialReference()
            proj4_str = "+proj=tmerc +lat_0=0 +lon_0=121 +k=0.9999 +x_0=250000 +y_0=0 +ellps=GRS80 +units=m +no_defs"
            spatialReference.ImportFromProj4(proj4_str)
            
            
            layer2 = ds2.CreateLayer(inFileStub, spatialReference,ogr.wkbLineString)
            
            ''' set up the fields '''
            fieldDefn = ogr.FieldDefn('name', ogr.OFTString)
            fieldDefn.SetWidth(250)
            layer2.CreateField(fieldDefn)  

            fieldDefn = ogr.FieldDefn('isisLbl', ogr.OFTString)
            fieldDefn.SetWidth(250)
            layer2.CreateField(fieldDefn) 
                                
            fieldDefn = ogr.FieldDefn('shorten', ogr.OFTInteger)
            layer2.CreateField(fieldDefn)    
            
            fieldDefn = ogr.FieldDefn('autoOrd', ogr.OFTInteger)
            layer2.CreateField(fieldDefn)    
                                                
            fieldDefn = ogr.FieldDefn('nextSect', ogr.OFTString)
            fieldDefn.SetWidth(250)
            layer2.CreateField(fieldDefn)  
             
            fieldDefn = ogr.FieldDefn('distNext', ogr.OFTReal)
            layer2.CreateField(fieldDefn)  
             
            fieldDefn = ogr.FieldDefn('year', ogr.OFTInteger)
            layer2.CreateField(fieldDefn)  

            fieldDefn = ogr.FieldDefn('accuracy', ogr.OFTString)
            fieldDefn.SetWidth(10)
            layer2.CreateField(fieldDefn) 
                         
            fieldDefn = ogr.FieldDefn('no_pnts', ogr.OFTInteger)
            layer2.CreateField(fieldDefn)  
            
            fieldDefn = ogr.FieldDefn('checked', ogr.OFTInteger)
            layer2.CreateField(fieldDefn)    
                         
            fieldDefn = ogr.FieldDefn('note', ogr.OFTString)
            fieldDefn.SetWidth(250)
            layer2.CreateField(fieldDefn)  
 
            fieldDefn = ogr.FieldDefn('comment', ogr.OFTString)
            fieldDefn.SetWidth(250)
            layer2.CreateField(fieldDefn)  
                                                         
            
            featDefn = layer2.GetLayerDefn()
                        
            
        for riverName,xSections in riverDict.items():
            #xSections.sort(reverse=True)                    
            xSections.sort(key=lambda section:section._section_number , reverse=True)     
            
            """ finalise the xSections in terms of sorting out the order""" 
            #the whole loop must be done first before exporting each cross-section 
            #due to the requirement for next section bed values. 
            for i, objXSection in enumerate(xSections):
                                    
                try:
                    #print objXSection._river_section_name, objXSection._section_number   
                    objXSection._section_number_derived = i               
                    objXSection._next_section = xSections[i+1]
                except IndexError:
                    #print 'Last section encountered: ' + str(objXSection)
                    pass
                 
                objXSection.derive_bank_bed()
                
                
            if type=='ied':
                outfile = os.path.join(os.path.split(infile)[0], riverName+'.ied')
                fo=open(outfile,'w')
                
            for i, objXSection in enumerate(xSections):
                

                try:
                    if type =='ied':
                        fo.write(objXSection.get_dat_format())        
                    elif type=='pnt':
                        try:
                            fo.write(objXSection._left_bank.get_point_xy_format())
                            fo.write(objXSection._right_bank.get_point_xy_format())
                        except:
                            pass
                        for pnt in objXSection._section_points:
                            try:
                                fo.write(pnt.get_point_xy_format())
                            except:
                                pass
                                
                    elif type=='shp':
                        if str(objXSection._river_section_name) =='114030_067':
                            pass
                
                        line = ogr.Geometry(ogr.wkbLineString) 
                        line.AddPoint(objXSection._section_points[0]._easting,objXSection._section_points[0]._northing)
                        line.AddPoint(objXSection._section_points[-1]._easting,objXSection._section_points[-1]._northing)

                        
                        feat2 = ogr.Feature(featDefn)
                        feat2.SetGeometry(line)
                        feat2.SetField('name', objXSection._river_section_name)
                        feat2.SetField('isisLbl', objXSection._node_lable)
                        feat2.SetField('shorten', objXSection._label_shorten)
                        if objXSection._next_section is not None:
                            feat2.SetField('nextSect', str(objXSection._next_section._river_section_name))
                        feat2.SetField('distNext', round(objXSection._dist_to_next,0))
                        feat2.SetField('year', objXSection._survey_year)
                        feat2.SetField('no_pnts', objXSection._no_of_points)
                        feat2.SetField('autoOrd', objXSection._auto_order)
                        feat2.SetField('note', objXSection._auto_note)
                        feat2.SetField('accuracy', objXSection._accuracy)                                           
                        layer2.CreateFeature(feat2)
                        feat2.Destroy()
            
                except Exception, e:
                    print 'Error in writing out:' + str(objXSection)
                    print e
                
            if type=='ied':
                fo.close()
        
        
        if type=='shp':
            ds2.Destroy()     
        print 'END'

def database_ops():        
    pass
    
    
if __name__ == '__main__':

    #read_survey_point_file(infile=r'.\test_files\nanao.csv',type='pnt')
    read_survey_point_file(infile=r'.\test_files\all_raw_data.csv',type='ied')
    