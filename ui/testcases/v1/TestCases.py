import os
import sys
sys.path.append(os.path.abspath("../")) 

import time
import unittest
import HTMLTestRunner  
from com.cavisson.driver.cavium import CavissonWebDriver,NSWebDriver 

class TestReporting(unittest.TestCase):
    @classmethod 
    def setUpClass(self):
        mCavissonWebDriver = CavissonWebDriver()
        #mCavissonWebDriver.htmlUnitDriver()
        mCavissonWebDriver.fireFoxDriver()
        self.driver = mCavissonWebDriver 
 
    def test_001_login_to_ns(self):
        self.driver.open("http://192.168.1.95")
        self.driver.takeScreenShot("login-before.png") 
        self.driver.waitForVisibility(30) 
        self.driver.doLogin("srvstva","srvstva") 
        self.driver.takeScreenShot("login-after.png") 

    def test_002_click_show_all_test_runs(self):
        self.driver.waitForVisibility(30) 
        self.driver.doShowAllTestRun()  
        self.driver.takeScreenShot("show-all-testruns.png")  

    def test_003_search_for_tr_5145(self):
        self.driver.waitForVisibility(30)
        self.driver.doSearchTestRun("5145") 
        self.driver.takeScreenShot("search-results.png")

    def test_004_view_reports_for_tr_5145(self):
        self.driver.waitForVisibility(30)
        self.driver.doSelectTRAndViewReports()
        self.driver.takeScreenShot("click-view-reports.png")
    
         
    def test_005_switch_windows(self):
        handle = self.driver.getWindowHandles()
        self.driver.switchTo(handle[1]) 
        title = self.driver.getTitle()
        expectedTitle="Netstorm - Report Selection - Test Run Number:\xa05145 (192.168.1.95:80)" 
        self.driver.takeScreenShot("switch-windows.png") 
        #self.assertEqual(title,expectedTitle)  
        self.assertIn("5145",title)  

    def test_006_open_custom_query_screen(self):
        self.driver.openCustomQueryScreen()
        time.sleep(5)  
        self.driver.selectObjectType("Flowpath")
        self.driver.takeScreenShot("open-custom-query.png")
    def test_007_open_flowpath_report(self):
        self.driver.selectObjectType("Flowpath")
        self.driver.runCustomQuery()
        time.sleep(5)
        self.driver.waitForVisibility(30) 
        self.driver.takeScreenShot("flowpath-report.png") 

    @unittest.skip("Skipping navigate back to custom query screen") 
    def test_008_navigate_back_to_custom_query_screen(self):
        self.driver.back()
        self.driver.waitForVisibility(30) 
        
    def test_009_open_transaction_report(self):
        self.driver.waitForVisibility(30)
        self.driver.openCustomQueryScreen()
        self.driver.selectObjectType("Transaction") 
        self.driver.runCustomQuery()
        time.sleep(5)
        self.driver.waitForVisibility(30)
        self.driver.takeScreenShot("transcation-report.png")
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
        self.driver.takeScreenShot("method-timing-report.png")
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
        runner = HTMLTestRunner.HTMLTestRunner(
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

