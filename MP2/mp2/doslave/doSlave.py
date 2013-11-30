# -*- coding: utf-8 -*-

""" 
Changes made to this version:
1) export the ascii results even if the model is failed
"""

import os
import subprocess
import sys

debug = True

if debug:
    sys.stdout.write('in python\n')
startingDir = os.getcwd()

modelDir = os.listdir('Model')[0]
if debug:
    sys.stdout.write('Changing dir to ' + os.path.join('Model', modelDir) + '\n')
os.chdir(os.path.join('Model', modelDir))

sErr = open('pyStderr.txt', 'w')
sIn = open(os.devnull, 'r')
sOut = open(os.devnull, 'r')
if debug:
    sys.stdout.write('Running ISIS 2D\n')
p = subprocess.Popen(['isis2d', '-s', '-q', 'model.xml'], stdin=sIn, stderr=sErr, stdout=sErr)

if debug:
    sys.stdout.write('Waiting for ISIS 2D to finish\n')
i2dErr = p.wait()

sErr.close()
sOut.close()
sIn.close()

if debug:
    sys.stdout.write('i2dErr is ' + str(i2dErr) + '\n')
    
ppErr = 0


# produce the resuls even if the run is failed with 112 
if i2dErr == 100 or i2dErr == 112:
# The model ran fine
    os.chdir('model_01')
    sErr = open('pyStderr.txt', 'w')
    sIn = open(os.devnull, 'r')
    sOut = open(os.devnull, 'r')
    
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

if debug:
    sys.stdout.write('Going back to ' + startingDir + '\n')
os.chdir(startingDir)

if debug:
    sys.stdout.write('Calling exit with code ' + str(i2dErr) + '\n')
if i2dErr != 100:
    sys.exit(i2dErr)
elif i2dErr == 100 and ppErr != 0:
    sys.exit(ppErr)
else:
    sys.exit(i2dErr)
