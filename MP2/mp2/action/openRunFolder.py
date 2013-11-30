import subprocess
from mp2.model.run import Run


def openRunFolder(runName):
    objRun = Run(runName)
    cmd = 'Explorer.exe ' + objRun._ModelFiles._folder_run
    try:
        subprocess.Popen(cmd)
    except Exception, e:
        print cmd
        print e

# openRunFolder('Ha001_Cat0001_Dom004_1000Yr_ND')
