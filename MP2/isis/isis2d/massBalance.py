
import os
import csv
import numpy

class MB(object):
    '''
    classdocs
    '''
    def __init__(self, mbFileName):
        self.mbFile = mbFileName
        self.isValid = False
        # TODO: Create Unit Testing for this and error trapping?

        if os.path.isfile(self.mbFile):
            csvFile = open(self.mbFile)
            csvReader = csv.DictReader(csvFile)           
        else:
            print 'no such file <%s>' %self.mbFile
            return

        self.time = []
        self.inflow = []
        self.outflow = []
        self.rateOfChange = []
        self.volume = []
        self.qe = []
        self.maxCourant = []
        self.wetCell = []
        self.mbErr = []
        self.posTrappedVol = []
        self.negTrappedVol = []

        for row in csvReader:

        # ['T', '%volErr', 'Wet Cells', 'Q->1D', 'Q BC->2D', 'Q BC<-2D', '2D dV/dt', '2D V',
        # 'Trapped(+)Vol', 'Trapped(-)Vol', 'Qe', ' ', 'cumulative2DInflowVol', 'cumulativeLinkInflowVol',
        #  'maxCourant']

            self.time.append(float(row['T']))
            self.mbErr.append(float(row['%volErr']))
            self.inflow.append(float(row['Q BC->2D']))
            self.outflow.append(float(row['Q BC<-2D']))
            self.rateOfChange.append(float(row['2D dV/dt']))
            self.volume.append(float(row['2D V']))
            self.posTrappedVol.append(float(row['Trapped(+)Vol']))
            self.negTrappedVol.append(float(row['Trapped(-)Vol']))
            self.qe.append(float(row['Qe']))
            self.maxCourant.append(float(row['maxCourant']))
            self.wetCell.append(int(row['Wet Cells']))
        csvFile.close()

        if self.maxCourant[-1] is None:
            # catch instance where MB writing is not complete:
            self.last_time_step_idx = -2
            self.last_time_step = self.time[self.last_time_step_idx]

        else:
            self.last_time_step_idx = -1
            self.last_time_step = self.time[self.last_time_step_idx]

        self.time_step = self.time[-1] - self.time[-2]

        self.isValid = True

    def calc_mb_pct_error_flow_rate(self, windowTime):
        '''
            Para : windowTime (S)
        '''
        qDict = dict()

        for i in range(-1, -len(self.time), -1):
            if self.time[i] <= self.time[-1] - windowTime:
                rowTimeStart = i
                break

        averageErrorFlow = numpy.mean(self.qe[rowTimeStart:])
        averageAbsErrorFlow = sum(numpy.abs(self.qe[rowTimeStart:])) / len(self.qe[rowTimeStart:])
        averageInflow = numpy.mean(self.inflow[rowTimeStart])

        qDict['mbErrorFlowPctCumMean'] = 100.0 * averageErrorFlow / averageInflow
        qDict['mbErrorFlowPctCumAbsMean'] = 100.0 * averageAbsErrorFlow / averageInflow

        qDict['mbErrorFlowPctAtTimeTMean'] = numpy.mean(numpy.array(self.qe[rowTimeStart:]) / numpy.array(self.inflow[rowTimeStart:]))
        qDict['mbErrorFlowPctAtTimeTStdev'] = numpy.std(numpy.array(self.qe[rowTimeStart:]) / numpy.array(self.inflow[rowTimeStart:]))

        # calculate the percentage change in volume over the windowTime
        qDict['dvPrcWindow'] = -100.0 + 100.0 * self.volume[rowTimeStart] / self.volume[-1]

        return qDict

    def analyse_last_time_step_customised(self):
        """
        @return: a dict with last timestep stats 
        """
        qDict = dict()

        if len(self.time) <= 10:
            qDict['time'] = -9999.9
            qDict['inflow'] = -9999.9
            qDict['outflow'] = -9999.9
            qDict['currentVolume'] = -9999.9
            qDict['rateOfChange'] = -9999.9
            qDict['rateOfChangeTwohr'] = -9999.9
            qDict['rateOfChangeFourhr'] = -9999.9
        else:
            qDict['time'] = self.time[self.last_time_step_idx] / 3600
            qDict['inflow'] = self.inflow [self.last_time_step_idx]
            qDict['outflow'] = self.outflow [self.last_time_step_idx]
            qDict['currentVolume'] = self.volume[self.last_time_step_idx]
            qDict['rateOfChange'] = float(sum(self.rateOfChange[-10:]) / len(self.rateOfChange[-10:]))

            if self.time[-1] > 3 * 3600:  # if time is greater than 3hrs
                qDict['rateOfChangeTwohr'] = float(sum(self.rateOfChange[-125:-115]) / len(self.rateOfChange[-125:-115]))
            else:
                qDict['rateOfChangeTwohr'] = -9999.9
            if self.time[-1] > 5 * 3600:  # if time is greater than 5hrs
                qDict['rateOfChangeFourhr'] = float(sum(self.rateOfChange[-245:-235]) / len(self.rateOfChange[-245:-235]))
            else:
                qDict['rateOfChangeFourhr'] = -9999.9

        return qDict

    def analyse_last_time_step(self):
        """
        @return: a dict with last timestep stats 
        """
        qDict = dict()

        qDict['timeInSecond'] = self.time[self.last_time_step_idx]
        qDict['timeInHr'] = self.time[self.last_time_step_idx] / 3600
        qDict['inflow'] = self.inflow [self.last_time_step_idx]
        qDict['outflow'] = self.outflow [self.last_time_step_idx]
        qDict['wetcells'] = self.wetCell[self.last_time_step_idx]
        qDict['currentVolume'] = self.volume[self.last_time_step_idx]
        qDict['mass_balance_err_perc'] = self.mbErr[self.last_time_step_idx]
        qDict['posTrappedVol'] = self.posTrappedVol[self.last_time_step_idx]
        qDict['negTrappedVol'] = self.negTrappedVol[self.last_time_step_idx]

        # qDict['rateOfChange'] = float(sum(self.rateOfChange[-10:]) / len(self.rateOfChange[-10:]))

        return qDict

    def flowOutWithin5PercentOfFlowIn(self):

        vIn = sum(self.inflow[-5:])
        vOut = sum(self.outflow[-5:])

        vIn /= 5.0
        vOut /= 5.0
        lowerRange = vIn * 0.95
        upperRange = vIn * 1.05
        if vOut > upperRange or vOut < lowerRange:
            return False
        return True

    def trappedVolsLessThan10PercentOfDomainVolume(self):
        posVol = self.posTrappedVol[-1]
        negVol = self.negTrappedVol[-1]
        totVol = self.volume[-1]
        if (posVol - negVol) > (0.1 * totVol):
            return False
        return True

    def gen_vol_plot(self):
        pass


if __name__ == '__main__':
    objMB = MB(r'.\test_files\MB.csv')
    print objMB.analyse_last_time_step()
    pass