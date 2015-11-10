import os
import sys
import time
import unittest

# This is required to add cavisson modules to path
# Modules are stored relative to testcases directory
sys.path.append(os.path.abspath("../")) 

from com.cavisson.util.HTMLTestRunner import HTMLTestRunner  
from com.cavisson.driver.v1.cavium import CavissonWebDriver,NSWebDriver 

class TestReporting(unittest.TestCase):
    @classmethod 
    def setUpClass(self):
        #mCavissonWebDriver = CavissonWebDriver()
        #mCavissonWebDriver = NSWebDriver("http://localhost:4444/wd/hub")
        mCavissonWebDriver = NSWebDriver("http://192.168.100.23:4444/wd/hub")
        #mCavissonWebDriver.htmlUnitDriver()
        #mCavissonWebDriver.fireFoxDriver()
        mCavissonWebDriver.remoteFireFoxDriver() 
        #mCavissonWebDriver.remoteIEDriver() 
        #mCavissonWebDriver.remoteChromeDriver() 
        #mCavissonWebDriver.remoteIEDriver() 

        self.driver = mCavissonWebDriver 
 
    def test_001_login_to_ns(self):
        #self.driver.open("http://192.168.1.95")
        #self.driver.takeScreenShot("png/login-before.png") 
        #self.driver.waitForVisibility(30) 
        self.driver.doLogin("http://192.168.1.95","srvstva","srvstva") 
        self.driver.takeScreenShot("png/login-after.png") 

    def test_002_click_show_all_test_runs(self):
        self.driver.waitForVisibility(30) 
        self.driver.doShowAllTestRun()  
        self.driver.takeScreenShot("png/show-all-testruns.png")  

    def test_003_search_for_tr_5145(self):
        self.driver.waitForVisibility(30)
        self.driver.doSearchTestRun("5145") 
        self.driver.takeScreenShot("png/search-results.png")

    def test_004_view_reports_for_tr_5145(self):
        self.driver.waitForVisibility(30)
        self.driver.doSelectTRAndViewReports()
        self.driver.takeScreenShot("png/click-view-reports.png")
        self.driver.waitForVisibility(30)
    
    @unittest.skip("")    
    def test_005_switch_windows(self):
        handle = self.driver.getWindowHandles()
        self.driver.switchTo(handle[1]) 
        title = self.driver.getTitle()
        expectedTitle="Netstorm - Report Selection - Test Run Number:\xa05145 (192.168.1.95:80)" 
        self.driver.takeScreenShot("png/switch-windows.png") 
        #self.assertEqual(title,expectedTitle)  
        self.assertIn("5145",title)  

    @unittest.skip("")
    def test_006_open_custom_query_screen(self):
        self.driver.openCustomQueryScreen()
        time.sleep(5)  
        #self.driver.selectObjectType("Flowpath")
        self.driver.takeScreenShot("png/open-custom-query.png")

    def test_007_open_flowpath_report(self):
        time.sleep(5)
        self.driver.openCustomQueryScreen()
        self.driver.waitForVisibility(30)
        time.sleep(5)
        self.driver.selectObjectType("FlowPath")
        self.driver.waitForVisibility(30)
        time.sleep(5)
        self.driver.runCustomQuery()
        time.sleep(5)
        self.driver.waitForVisibility(30) 
        self.driver.takeScreenShot("png/flowpath-report.png") 
        self.driver.saveResponse("response/flowpath-report.html")
        diff = self.driver.compareFiles("response/flowpath-report.html",
                                "response/baseline/flowpath-report.html")
        self.assertFalse(diff)
        self.assertTrue(diff)

    @unittest.skip("Skipping navigate back to custom query screen") 
    def test_008_navigate_back_to_custom_query_screen(self):
        self.driver.back()
        self.driver.waitForVisibility(30) 
        
    def test_009_open_transaction_report(self):
        self.driver.waitForVisibility(30)
        self.driver.openCustomQueryScreen()
        self.driver.selectObjectType("Transactions") 
        self.driver.runCustomQuery()
        time.sleep(5)
        self.driver.waitForVisibility(30)
        self.driver.takeScreenShot("png/transcation-report.png")
        self.assertIsNotNone(self.driver)
        source = self.driver.getPageSource()
        transaction_name = self.driver.webFind("title=\"CrsHomePage\" class=\"tableCell\">","</a0:td>", source)
        self.assertEqual(transaction_name, "CrsHomePage")
        self.driver.back()  

    @unittest.skip("Skipping navigate back to custom query screen") 
    def test_010_navigate_back_to_custom_query_screen(self):
        self.driver.back()
        self.driver.waitForVisibility(30)
        #self.driver.switchWindows() 
        #self.driver.close()  
   
    def test_011_open_method_timings(self):
        self.driver.waitForVisibility(30)
        self.driver.openCustomQueryScreen()
        self.driver.selectObjectType("Method Timing") 
        self.driver.waitForVisibility(30)
        time.sleep(5)
        self.driver.runCustomQuery() 
        self.driver.waitForVisibility(30)
        self.driver.takeScreenShot("png/method-timing-report.png")
        source = self.driver.getPageSource()
        toFind = self.driver.webFind('title="weblogic.jdbc.wrapper" class="tableCell">','</a0:td>',source) 
        self.assertEqual("weblogic.jdbc.wrapper",toFind)
        self.driver.back() 
         
    def test_012_open_db_requests(self):
        self.driver.waitForVisibility(30)
        self.driver.openCustomQueryScreen()
        self.driver.waitForVisibility(30)
        self.driver.selectObjectType("DB Request")
        time.sleep(5)
        self.driver.runCustomQuery()
        self.driver.waitForVisibility(30)
        time.sleep(10)
        self.driver.back()

    @classmethod 
    def tearDownClass(self):
        if self.driver: 
            self.driver.quit() 


class TestRunner(unittest.TestCase):
    
    def test_main(self):
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(TestReporting),
            ])
        filename = "reports/NetdiagnosticsTestReport_%d.html" %(int(time.time())) 
        fp = file(filename, "wb")
        runner = HTMLTestRunner(
                    stream=fp,
                    title='NetDiagnostics Automation Unit Test Report',
                    description='Report for NetDiagnostics'
                    )

        runner.run(self.suite)     
        
        
class BasicTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        mWebDriver = NSWebDriver("http://localhost:4444/wd/hub")
        mWebDriver.remoteFireFoxDriver()
        self.driver = mWebDriver
        
    def test_openLocalHost(self):
        self.driver.doLogin("http://192.168.1.95","srvstva", "srvstva") 

         
    @classmethod 
    def tearDownClass(self):
        if not self.driver:
            return 

        self.driver.quit() 

