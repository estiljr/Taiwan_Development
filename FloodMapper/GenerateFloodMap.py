import subprocess
import os

isisMapper = r"C:\isis\bin\ISISMapper.exe"

def GenerateFloodMap(tinFile, csvFile, dtmFile, timeSnaps, modelFolder):
    """Generates depth grid and flood extent shapefile from the model result."""

    
    outDir = modelFolder+'\FloodMaps'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    outGridFile = outDir+'\output_depth.asc'
    try:
        args = 'calculate1dflooddepth /i: ',dtmFile+','+tinFile+','+csvFile+','+timeSnaps, ' /o: ',outGridFile
        subprocess.call([isisMapper, args],shell=True)
        ts = timeSnaps.split(",")
        if len(ts) == 1: # if only 1 timeSnap specified
            outShapefile = GridToShapefile(outGridFile,modelFolder)
        elif len(ts) > 1: # if generating floodmaps for several timeSnaps
            for t in ts:
                outGridFile = outDir+'\output_depth_TS'+t+'.asc'
                outShapefile = GridToShapefile(outGridFile,modelFolder)
    except ValueError as e: print(e)
    # Possible exception: csv file open, throws an error
    if os.path.exists(outGridFile) and os.path.exists(outShapefile):
        isSuccessful = True; 
        message = "Flood maps generation completed!"
    else: isSuccessful = False; message = "Flood maps generation failed!"

    return (isSuccessful,message)


def GridToShapefile(gridFile, modelFolder):
    """Converts grid to a shapefile format."""

    outDir = modelFolder+'\FloodMaps'
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    fileName = os.path.splitext(os.path.basename(gridFile))[0]
    print(fileName)
    outShapefile = outDir+'\\'+fileName+'.shp'
    try:
        args = '-extractfloodextent /i: ',gridFile,' /o: ',outShapefile
        subprocess.call([isisMapper, args],shell=True)
    except ValueError as e: print(e)
    return outShapefile


if __name__=='__main__':

    tinFile = r"isis\isismapper\test_files\tin_related\xsection4_TIN.htn" 
    csvFile = r"isis\isismapper\test_files\tin_related\xsection4.csv" 
    dtmFile = r"isis\isismapper\test_files\tin_related\dtm_pilot_taipei.asc" 
    timeSnaps = "1,2" 
    outFile = r"isis\isismapper\test_files\tin_related"
    output = GenerateFloodMap(tinFile, csvFile, dtmFile, timeSnaps, outFile)
    print(output)

