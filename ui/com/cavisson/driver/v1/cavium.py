# -*- coding: iso-8859-15 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from selenium.webdriver.support.ui import Select 
import filecmp 

class CavissonWebDriver(object):
    '''
    Plain webdriver implementation for Cavisson Suite of products
    Contains utility functions for accessing elements of a webpage
    '''

    # The selenium grid URL. Defaults to localhost 
    cSeleniumGridURL = "http://127.0.0.1:4444/wd/hub" 

    def __init__(self, pSeleniumGridURL = "http://127.0.0.1:4444/wd/hub"):
        self.driver = None
        self.cSeleniumGridURL = pSeleniumGridURL  
        

            
    def fireFoxDriver(self):
        '''
        registers a new firefox browser driver 
        ''' 
        try:
            self.driver = webdriver.Firefox()
        except Exception as e:
            return False 
     
        return True 
   
    def htmlUnitDriver(self,capabilities = DesiredCapabilities.HTMLUNIT):
        '''
        Registers a new light weight HTMLUNIT driver. This is less
        resource intensive, but lacks many features..such as taking
        snapshots etc.
        ''' 
        try: 
            self.driver = webdriver.Remote(self.cSeleniumGridURL,capabilities) 
        except Exception as e:
            return False 
        
        return True 

    def remoteFireFoxDriver(self):
        '''
        Registers a firefox driver from a remote selenium grid url 
        This can be used to open the browser on remote machines
        '''
        self.driver = webdriver.Remote(self.cSeleniumGridURL,DesiredCapabilities.FIREFOX)

    def remoteIEDriver(self):
        self.driver = webdriver.Remote(self.cSeleniumGridURL,DesiredCapabilities.INTERNETEXPLORER)

    def remoteChromeDriver(self): 
        self.driver = webdriver.Remote(self.cSeleniumGridURL,DesiredCapabilities.CHROME)

    def remoteOperaDriver(self):
        self.driver = webdriver.Remote(self.cSeleniumGridURL,DesiredCapabilities.OPERA)

    def open(self,url):
        '''
        Navigates to specified URL using the appropriate webdriver 
        ''' 
        self.driver.get(url)

    def findElementByXPath(self,pXPath):
        '''
        Returns the HTML dom element found using xpath
        ''' 
        return (self.driver.find_element_by_xpath(pXPath)) 


    def findElementByXPathAndSendKeys(self,pXPath, pKey):
        '''
        Sends the specified keys/text to the element
        You may want to send login credentials to a login form.  
        '''  
        self.findElementByXPath(pXPath).send_keys(pKey)
 
    def findElementByXPathAndDoClick(self,pXPath):
        '''
        Clicks on a clickable element. Example - Search Button
        ''' 
        self.findElementByXPath(pXPath).click() 

    
    def findElementByID(self,pId):
        '''
        Returns the html element identified by its id 
        Eg: - 
            <h1 id='header'>This is a header text</h1> 
        '''
        return (self.driver.find_element_by_id(pId))


    def findElementByIDAndSendKeys(self,pId,pKey):
        '''
        Sends the specified keys/text to the element
        '''
        self.findElementByID(pId).send_keys(pKey)


    def findElementByIDAndDoClick(self,pId):
        '''
        Clicks on a clickable element
        '''
        self.findElementByID(pId).click()

    def waitForVisibility(self,pSeconds):
        '''
        Impose a wait on the browser to wait till visible links appear
        ''' 
        self.driver.implicitly_wait(pSeconds) 

   
   
    def takeScreenShot(self,filename):
        '''
        Takes screen shot of the current page and saves in a file
        ''' 
        self.driver.get_screenshot_as_file(filename) 


    def getTitle(self):
        '''
        Returns the title of the current active window
        ''' 
        return self.driver.title
        
    def getPageSource(self, encode = True):
        '''
        Returns the whole HTML source code as string
        ''' 
        mPageSource = self.driver.page_source
        if encode != True:
            return mPageSource

        return mPageSource.encode("utf-8")

    def saveResponse(self, pFileName):
        '''
        Saves the entire source file to disk
        '''
        with open(pFileName, 'wb') as file:
            file.write(self.getPageSource())
            

    def compareFiles(self, pFirstFile, pSecondFile):
        '''
        Compares two files and checks for diff. 
        Returns False if files are different
        else True if both the file are same
        '''
        mDiffFlag = False
        try:
            # Throws exception when file is not found.
            mDiffFlag = filecmp.cmp(pFirstFile, pSecondFile)
        
        except Exception as e:
            return False 

        return mDiffFlag
         
    def webFind(self, pLb, pRb, pString):
        '''
        Checkpoint for finding a string between a given left and right
        bound. Returns string on the first match
        //TODO Implement using a regex 
        '''
        mLbLen = len(pLb)

        # Replace all newline with spaces
        mString = pString.replace('\n', ' ').replace('\r', '')
      
        mLBIdx = mString.find(pLb)
       
        # Index not found. No match for given LB
        if mLBIdx == -1:
            return "LB_NOT_FOUND"

        # Match found. Create a substring starting from the given LB
        mString = mString [ mLBIdx : ] 
        
        # Search for RB in the newly created String
        mRBIdx = mString.find(pRb)
      
        # Return if RB not found. No match
        if mRBIdx == -1:
            return "RB_NOT_FOUND"

        # Return the string between LB & RB 
        mString = mString[ (0 + mLbLen) : mRBIdx ].strip()

        # Somehow String is empty or NULL for given LB & RB 
        # Return 
        if not mString:
           return "STRING_NOT_FOUND"

        # Return the matched string
        return mString


    def getWindowHandles(self):
        '''
        Get all active window handles and store them in a hashmap
        Returns a map of all window handles starting from id 0 to n 
            0 - The main window (Test run GUI)
            1 - The reporting window
            2 - Custom query screen
            3 - Future
        The map is updated each time this method is called. 
        //TODO Can we have a name value pair for to identify windows
        ''' 
        # Get all window handles 
        windows = self.driver.window_handles 
        i = 0
        windowHandlesMap = {}  # Initialize an empty window map
        for window in windows:
            windowHandlesMap[i] = window # put the window in the map
            i += 1 

        # Return the map containing window handles
        return windowHandlesMap 
       
    def switchTo(self,pHandle):
        '''
        Switch to specific window handle
        ''' 
        self.driver.switch_to_window(pHandle) 


    def back(self):
        '''
        Navigates back in the history to one place
        ''' 
        self.driver.back() 

    def forward(self):
        '''
        Navigates one step forward in the history
        ''' 
        self.driver.forward() 
 
    def quit(self):
        '''
        Closes all running instances of browser. This closes even the popups 
        ''' 
        if self.driver: 
            self.driver.quit() 
  
    def close(self):
        '''
        Closes only first instance of the browser
        ''' 
        if self.driver:
            self.driver.close() 
            
            
            
class NSWebDriver(CavissonWebDriver):
    '''
    Implementation of CavissonWebDriver for Netstorm product
    Contains methods specific to Netstorm UI 
    '''
    def __init__(self,pSeleniumGridURL = CavissonWebDriver.cSeleniumGridURL):
        super(NSWebDriver,self).__init__(pSeleniumGridURL)



    def doLogin(self,pURL, pUserId, pPassword):
        ''' 
        Performs login to NS/NDE box using the specified credentials 
        '''
        try:
            self.open(pURL)
            self.findElementByXPathAndSendKeys(".//*[@id='Userid']", pUserId)
            self.findElementByXPathAndSendKeys(".//*[@id='Password']", pPassword)
            self.findElementByXPathAndDoClick(".//*[@id='frmMain']/div[2]/table[2]/tbody"
                                           "/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td/input[1]")
        except Exception as e:
            pass  

    def doShowAllTestRun(self):
        '''
        Shows all test runs. This should be called after successfull login or else
        it will fail to find the show_all element  
        ''' 
        self.findElementByXPathAndDoClick(".//*[@id='middlePart']/tbody/tr[1]/td/table/tbody/"
                                          "tr[1]/td[3]/table/tbody/tr/td[3]/input")

    def doSearchTestRun(self,pTestIdx):
        '''
        Searches for the specified testidx
        '''
        mWebElement = self.findElementByXPath(".//*[@id='middlePart']/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/table/tbody/tr[2]/td[5]/input")
        mWebElement.send_keys(pTestIdx)
    
        self.findElementByXPathAndDoClick(".//*[@id='middlePart']/tbody/tr[1]/td/table/tbody/tr[1]/td[3]/table/tbody/tr/td[1]/input")
    


    def doSelectTRAndViewReports(self):
        '''
        Select the specified test run and opens the reporting window
        ''' 
        
        # Select Checkbox for searched TR XPATH = .//*[@id='RowId1']/td[1]/input
        self.findElementByXPathAndDoClick(".//*[@id='RowId1']/td[1]/input")
     
        # Find XPATH for VIEW REPORTS button and click on it. 
        # XPATH =.//*[@id='middlePart']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/
        #        table/tbody/tr/td[2]/table/tbody/tr/td/input[5]
        # 
        self.findElementByXPathAndDoClick(".//*[@id='middlePart']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/"
                                          "tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/input[5]")


    
    def runCustomQuery(self):
        '''
        Runs the specified query by clicking on the run button
        ''' 
        self.findElementByXPathAndDoClick(".//*[@id='runId']") 

    
    def openCustomQueryScreen(self):
        '''
        Opens up the custom query window
        '''
        # First switch to the new window i,e custom query screen 
        handle = self.getWindowHandles()
        self.switchTo(handle[1]) # handle[1] is the reporting screen
        # Click on add button 
        self.findElementByXPathAndDoClick(".//*[@id='add']")

    def selectObjectType(self,pObject):
        '''
        Selects the specified object from the drop down list
        Object can be one among the following 
            1. URL
            2. Page
            3. Transactions
            4. FlowPath
            5. Sessions 
            6. Logs
            7. DB Request
            8. Service
            9. Method Timing
            10. Exceptions 
        ''' 
        #self.switchWindows()
        handle = self.getWindowHandles()
        #print [handle[k] for k in handle.keys()]
        self.switchTo(handle[2]) # handle[2] is the custom query screen

        #self.findElementByXPathAndSendKeys(".//*[@id='middlePart']/tbody/tr/td/fieldset/"
        #                         "table[1]/tbody/tr[3]/td[1]/table/tbody/tr[1]/"
        #                          "td/table/tbody/tr[2]/td/select", pObject)
        
        #element = self.driver.find_element_by_name("chkObjType")
        #print "element = ",element
        #for option in element.find_element_by_tag_name("option"):
        #    if option.text == pObject:
        #        option.click() 
    
    
        # The above commented portion is not working.. this is the best solution till date.
        select = Select(self.findElementByXPath(".//*[@id='middlePart']/tbody"
                                                "/tr/td/fieldset/table[1]/tbody"
                                                "/tr[3]/td[1]/table/tbody/tr[1]"
                                                "/td/table/tbody/tr[2]/td/select"))
        select.select_by_visible_text(pObject)
