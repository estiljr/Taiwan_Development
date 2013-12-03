import subprocess
import os

isisMapper = r"C:\isis\bin\ISISMapper.exe"

def GenerateFloodMap(tinFile, csvFile, dtmFile, timeSnaps, outGridFile):
    """Generates depth grid and flood extent shapefile from the model result."""

    try:
        TinToGrid(tinFile, csvFile, dtmFile, timeSnaps, outGridFile)
        ts = timeSnaps.split(",")
        if len(ts) == 1: # if only 1 timeSnap specified
            outGrid = outGridFile
            outShape = os.path.splitext(outGridFile)[0]+".shp"
            GridToShapefile(outGridFile,outShape)
        elif len(ts) > 1: # if generating floodmaps for several timeSnaps
            for t in ts:
                outGrid = os.path.splitext(outGridFile)[0]+"_TS"+t+'.asc'
                outShape = os.path.splitext(outGrid)[0]+".shp"
                GridToShapefile(outGrid,outShape)
    except ValueError as e: print(e)
    # Possible exception: csv file open, throws an error
    if os.path.exists(outGrid) and os.path.exists(outShape):
        isSuccessful = True; 
        message = "Flood maps generation completed!"
    else: isSuccessful = False; message = "Flood maps generation failed!"

    return (isSuccessful,message)




def TinToGrid(tinFile, csvFile, dtmFile, timeSnaps, outGridFile):
    """Generates depth grid from the model result."""

    try:
        args = 'calculate1dflooddepth /i: ',dtmFile+','+tinFile+','+csvFile+','+timeSnaps, ' /o: ',outGridFile
        subprocess.call([isisMapper, args],shell=True)
    except ValueError as e: print(e)
        

def GridToShapefile(gridFile, outShapefile):
    """Converts grid to a shapefile format."""

    try:
        args = '-extractfloodextent /i: ',gridFile,' /o: ',outShapefile
        subprocess.call([isisMapper, args],shell=True)
    except ValueError as e: print(e)


if __name__=='__main__':

    tinFile = r"isis\isismapper\test_files\tin_related\xsection4_TIN.htn" 
    csvFile = r"isis\isismapper\test_files\tin_related\xsection4.csv" 
    dtmFile = r"isis\isismapper\test_files\tin_related\dtm_pilot_taipei.asc" 
    timeSnaps = "1" 
    outFile = r"isis\isismapper\test_files\tin_related\depth.asc"
    output = GenerateFloodMap(tinFile, csvFile, dtmFile, timeSnaps, outFile)
    print(output)

