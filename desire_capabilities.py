from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
   command_executor='http://10.10.30.37:5000',
   desired_capabilities={'browserName': 'CHROME',
                         'version': '43',
                        'javascriptEnabled': True})
#driver = webdriver.Remote(
#   command_executor='http://127.0.0.1:4444/wd/hub',
#   desired_capabilities=DesiredCapabilities.OPERA)

#driver = webdriver.Remote(
#   command_executor='http://127.0.0.1:4444/wd/hub',
#   desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
