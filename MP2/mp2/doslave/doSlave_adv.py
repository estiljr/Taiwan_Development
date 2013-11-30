# -*- coding: utf-8 -*-

"""
  TBC - A set of scripts for automating ISIS 2D modelling.
  
  Copyright (C) 2012 Peter Wells for Lutra Consulting
  
  peter [dot] wells [at] lutraconsulting.co.uk
  http://www.lutraconsulting.co.uk/contact

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
# from lxml import etree
import os
import subprocess
import sys
import shutil

#===============================================================================
# def updateXML(solver,ts):
#     ISIS2D_NS = 'http://www.halcrow.com/ISIS2D'
#     ISIS2D = '{%s}' % ISIS2D_NS
#     NSMAP = {'i2d' : ISIS2D_NS}
# 
#     xmlFile = open('model.xml', 'r')
#     parser = etree.XMLParser(remove_blank_text = True)  # @UndefinedVariable
#     tree = etree.parse(xmlFile, parser)  # @UndefinedVariable
#     xmlFile.close()
#         
#     if 'adi' in solver:
#         solverElem = tree.find('i2d:domain/i2d:run_data/i2d:scheme', namespaces = NSMAP)
#         solverElem.text = "ADI"
#     if 'tvd' in solver:
#         solverElem = tree.find('i2d:domain/i2d:run_data/i2d:scheme', namespaces = NSMAP)
#         solverElem.text = "TVD"
#     else:
#         solverElem = tree.find('i2d:domain/i2d:run_data/i2d:scheme', namespaces = NSMAP)
#         solverElem.text = "ADI"
# 
#     timeStepElem = tree.find('i2d:domain/i2d:run_data/i2d:time_step', namespaces = NSMAP)
#     timeStepElem.text = str(ts)
# 
#     destinationXMLFileName = 'model.xml'
#     tree.write(destinationXMLFileName, pretty_print = True)
#===============================================================================

def updateXML(solver,ts):

    xmlTemp = open('model_tmp.xml',"w")
    xmlFile = open('model.xml','r')
    
    if 'adi' in solver:
        solver = 'ADI'
    elif 'tvd' in solver:
        solver = 'TVD'
    else:
        solver = 'ADI'
        
    lines = xmlFile.readlines()
    for line in lines:
        if "<time_step>" in line:
            currentTS  = line.split("<")[1].split(">")[1]
            newline = line.replace(str(currentTS),str(ts))
            line = newline              
        elif '<scheme>' in line:
            currentScheme = line.split("<")[1].split(">")[1]
            newline = line.replace(currentScheme,solver)
            line = newline              
        elif '<correct_negative_depths/>' in line and solver =='TVD':
            continue
        xmlTemp.write(line)       
        
    xmlTemp.close()
    xmlFile.close()
    os.remove('model.xml')
    os.rename('model_tmp.xml', 'model.xml')
        
        
def next_ts_solver(solver, currentTs):
    
    if 'tvd' in solver:
        if currentTs > 1.0:
            return 'tvd', 1.0
        elif currentTs > 0.75:
            return 'tvd', 0.75
        elif currentTs > 0.5:
            return 'tvd', 0.5
        elif currentTs > 0.25:
            return 'tvd', 0.25
        elif currentTs > 0.2:
            return 'tvd', 0.2
        elif currentTs > 0.125:
            return 'tvd', 0.125
        elif currentTs > 0.1:
            return 'tvd', 0.1
        else:
            ''' This is used to flag that the model shouldn't be run with a shortened TS '''
            return 'tvd', 0.0  
    elif 'adi' in solver: 
        if currentTs > 5.0:
            return 'adi', 5.0
        elif currentTs > 2.0:
            return 'adi',2.0
        elif currentTs > 1.0:
            return 'adi',1.0
        elif currentTs >  0.5:
            return 'adi', 0.5
        elif currentTs >  0.25:
            return 'adi', 0.25
        else:
            return 'tvd' , 1  

def run_model():        

    sys.stdout.write('start running model\n')
    startingDir = os.getcwd()
    
    fo = open('mode.txt' ,'r')
    mode = fo.readline().strip().split('=')[1]
    solver =fo.readline().strip().split('=')[1]
    ts = fo.readline().strip().split('=')[1]
    totalTry = fo.readline().strip().split('=')[1]
    fo.close()
    modelDir = os.listdir('Model')[0]
    
    sys.stdout.write('Changing dir to ' + os.path.join('Model', modelDir) + '\n')
    sys.stdout.write('running mode : ' + mode+ '\n')   
    os.chdir(os.path.join('Model', modelDir))
    
    ppErr = 0
    count=0
    while count < totalTry:
        count +=1
        
        sys.stdout.write('No [%s/%s] try running model\n'  %(count,totalTry))
                
        sErr = open('pyStderr.txt', 'w')
        sIn = open(os.devnull, 'r')
        sOut = open(os.devnull, 'r')
        
       
        sys.stdout.write('Running ISIS 2D\n')
        p = subprocess.Popen(['isis2d', '-s', '-q', 'model.xml'], stdin=sIn, stderr=sErr, stdout=sErr)
        
        
        i2dErr = p.wait()
        
        sErr.close()
        sOut.close()
        sIn.close()       
            
        if i2dErr == 100:
            sys.stdout.write('Model ran successfully\n')
            post_process()
            break
        else:    
            sys.stdout.write('i2dErr is ' + str(i2dErr) + '\n')
            solver,ts = next_ts_solver(solver,ts)
            sys.stdout.write('Use new solver[%s] and new time step [%s]\n'  %(solver,ts))
            if ts ==0:
                break
            else:
                updateXML(solver,ts)    
                
    sys.stdout.write('Going back to ' + startingDir + '\n')
    os.chdir(startingDir)
    

    sys.stdout.write('Calling exit with code ' + str(i2dErr) + '\n')
    if i2dErr != 100:
        sys.exit(i2dErr)
    elif i2dErr == 100 and ppErr != 0:
        sys.exit(ppErr)
    else:
        sys.exit(i2dErr)
        
def post_process():
    # The model ran fine
    os.chdir('model_01')
    sErr = open('pyStderr.txt', 'w')
    sIn = open(os.devnull, 'r')
    sOut = open(os.devnull, 'r')
    
    debug = True
    ppErr = 0
    if ppErr == 0:
        if debug:
            sys.stdout.write('Running ISIS2D_to_asc.exe\n')
        p = subprocess.Popen(['isis2d_to_asc.exe', '01.2dm', '01_waterlevel.dat', 'last'], stdin=sIn, stderr=sErr, stdout=sErr)
        if debug:
            sys.stdout.write('Waiting for ISIS2D_to_asc.exe to finish\n')
        ppErr = p.wait()
        
    if ppErr == 0:
        if debug:
            sys.stdout.write('Running ISIS2D_to_asc.exe\n')
        p = subprocess.Popen(['isis2d_to_asc.exe', '01.2dm', '01_depth.dat', 'last'], stdin=sIn, stderr=sErr, stdout=sErr)
        if debug:
            sys.stdout.write('Waiting for ISIS2D_to_asc.exe to finish\n')
        ppErr = p.wait()
        
    if ppErr == 0:
        if debug:
            sys.stdout.write('Running ISIS2D_to_asc.exe\n')
        p = subprocess.Popen(['isis2d_to_asc.exe', '01.2dm', '01_velocity.dat', 'last'], stdin=sIn, stderr=sErr, stdout=sErr)
        if debug:
            sys.stdout.write('Waiting for ISIS2D_to_asc.exe to finish\n')
        ppErr = p.wait()
        
    if ppErr == 0:
        if debug:
            sys.stdout.write('Running ISIS2D_to_asc.exe\n')
        p = subprocess.Popen(['isis2d_to_asc.exe', '01.2dm', '01_froude.dat', 'last'], stdin=sIn, stderr=sErr, stdout=sErr)
        if debug:
            sys.stdout.write('Waiting for ISIS2D_to_asc.exe to finish\n')
        ppErr = p.wait()
    
    if ppErr == 0:
        if debug:
            sys.stdout.write('Running ISIS2D_to_asc.exe\n')
        p = subprocess.Popen(['isis2d_to_asc.exe', '01.2dm', '01_hazard.dat', 'last'], stdin=sIn, stderr=sErr, stdout=sErr)
        if debug:
            sys.stdout.write('Waiting for ISIS2D_to_asc.exe to finish\n')
        ppErr = p.wait()
        
    if ppErr == 0:
        # Convert the depth grid to an extent
        depthFileName = None
        for filename in os.listdir('.'):
            if filename.startswith('01_depth_') and filename.endswith('.asc'):
                depthFileName = filename
                break
        if depthFileName is None:
            # Could not find depth file
            ppErr = 202
        else:
            inFile = open(depthFileName, 'r')
            outFile = open('extent_grid.asc', 'w')
            lineCounter = 0
            noData = ''
            for line in inFile:
                if lineCounter == 5:
                    noData = line.split()[1]
                if lineCounter < 6:
                    outFile.write(line)
                else:
                    vals = line.split()
                    for val in vals:
                        if val == noData:
                            outFile.write(noData + ' ')
                        else:
                            outFile.write('1 ')
                    outFile.write('\n')
                lineCounter += 1
            inFile.close()
            outFile.close()
            if debug:
                sys.stdout.write('Running gdal_polygonize.exe\n')
            p = subprocess.Popen(['gdal_polygonize.exe', 'extent_grid.asc', '-f', 'ESRI Shapefile', 'flood_extent.shp'], stdin=sIn, stderr=sErr, stdout=sErr)
            if debug:
                sys.stdout.write('Waiting for gdal_polygonize.exe to finish\n')
            ppErr = p.wait()
        
    
        sErr.close()
        sOut.close()
        sIn.close()
if __name__ == '__main__':
    run_model()