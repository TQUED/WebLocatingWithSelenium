import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class MMTTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_book_ticket(self):
        driver = self.driver
        driver.get("http://www.makemytrip.com/")
        self.assertIn("MakeMyTrip,", driver.title)
        time.sleep(10)
        select = Select(driver.find_element_by_id('from_typeahead1')) 
        select.select_by_visible_text('Goa, India (GOI)')
        time.sleep(5) 
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
