

import unittest
from condor.condor import CondorLog  



class Test(unittest.TestCase):


    def test_log_success(self):
        objLog = CondorLog('test_files\slave_successs.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('terminated', status)
        self.assertEquals(100, retCode)

    def test_log_cancelled(self):
        objLog = CondorLog('test_files\slave_cancelled.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('cancelled', status)
        self.assertEquals(None, retCode)
        
    def test_log_abnormal(self):
        objLog = CondorLog('test_files\slave_ctrl_c.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('terminated', status)
        self.assertEquals(-1073741819, retCode)

    def test_log_issues(self):
        objLog = CondorLog('test_files\slave_issues.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('running', status)
        self.assertEquals(None, retCode)

    def test_log_running(self):
        objLog = CondorLog('test_files\slave_startrunning.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('running', status)
        self.assertEquals(None, retCode)

    def test_log_submitted(self):
        objLog = CondorLog('test_files\slave_submitted.log')
        status,retCode = objLog.get_status_retcode()
        self.assertEquals('submitted', status)
        self.assertEquals(None, retCode)
                                        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()