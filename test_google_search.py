import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_google_page(self):
        driver = self.driver
        driver.get("http://10.10.30.37:5000")
        self.assertIn("Welcome to Analytics", driver.title)
        time.sleep(10)
        elem = driver.find_element_by_id("download-button")
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        uname = driver.find_element_by_name("username")
        uname.send_keys("admin")
        passd = driver.find_element_by_name("password")
        passd.send_keys("admin")
        time.sleep(10)
        login = driver.find_element_by_css_selector(".button.primary")
        login.send_keys(Keys.RETURN)
        time.sleep(10)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
