# -*- coding: utf-8 -*-

import os
import subprocess
import numpy as np

from sepaErrors import *

class AutoQA():


    def __init__(self):
        pass





    def __froudeLessThan1(self, modelRootDir, asciiTime):
        froudeFileName = os.path.join(modelRootDir, 'model_01', '01_froude_' + asciiTime + '.asc')
        if not os.path.isfile(froudeFileName):
            return False
        minVal, maxVal = self.minMax(froudeFileName)
        if maxVal > 1.0:
            return False
        return True

    def maxFroude(self, modelRootDir, asciiTime):  # ## Function added by Neil
        froudeFileName = os.path.join(modelRootDir, 'model_01', '01_froude_' + asciiTime + '.asc')
        if not os.path.isfile(froudeFileName):
            return
        minVal, maxVal = self.minMax(froudeFileName)
        return maxVal


    def __froudeLess90PercentileLessThan1(self, modelRootDir, asciiTime):
        froudeFileName = os.path.join(modelRootDir, 'model_01', '01_froude_' + asciiTime + '.asc')
        if not os.path.isfile(froudeFileName):
            return False
        percentile = self.__percentile(froudeFileName, 90)
        if percentile > 1.0:
            return False
        return True



    def __velocityLessThan10ms(self, modelRootDir, asciiTime):
        velocityFileName = os.path.join(modelRootDir, 'model_01', '01_velocity_' + asciiTime + '.asc')
        if not os.path.isfile(velocityFileName):
            return False
        minVal, maxVal = self.minMax(velocityFileName)
        if maxVal > 10.0:
            return False
        return True


    def __depthLessThan10m(self, modelRootDir, asciiTime):
        depthFileName = os.path.join(modelRootDir, 'model_01', '01_depth_' + asciiTime + '.asc')
        if not os.path.isfile(depthFileName):
            return False
        minVal, maxVal = self.minMax(depthFileName)
        if maxVal > 10.0:
            return False
        return True

    def __percentile(self, fileName, desiredPercentile):

        a = self.readAsciiFile(fileName)
        return np.percentile(a, desiredPercentile)



