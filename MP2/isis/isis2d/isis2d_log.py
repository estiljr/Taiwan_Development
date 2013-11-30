import os


class ISIS2D_Log(object):
    
    def __init__(self,logName):
        self.logName = logName
        self.isValid = False
        # Update the runs table with some stats about this run from 
        #logFileName = os.path.join(self.__running_sim_folder, modelFolder, 'Model', modelFolder, 'model.log')
        if os.path.isfile(self.logName):
            logFile = open(self.logName, 'r')
            self.convergenceTime = None
            self.maxCourant = None
            self.runTime = None
            
            lines= logFile.readlines()
            for line in lines:
                if line.startswith('Model successfully converged at'):
                    self.convergenceTime = float(line.split()[-2].strip())
                elif line.startswith('Maximum Courant number seen:'):
                    line = logFile.next()
                    self.maxCourant = float(line.split('  Domain  1: ')[1].split()[0].strip())
                elif line.startswith('Run completed in'):
                    self.runTime = float(line.split()[-2].strip())

            logFile.close()
            self.isValid = True
    
    def analyse_log_info(self):
        """
        @summary: return the fields as dictionary
        """
        if self.isValid:
            tmpDic=dict() 
              
            tmpDic['time_to_converge_hr'] = self.convergenceTime
            tmpDic['max_courant'] = self.maxCourant
            tmpDic['simulation_time_hr'] =self.runTime / 3600.0
            return tmpDic