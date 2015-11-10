import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class MMTTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_book_ticket(self):
        driver = self.driver
        driver.get("http://www.makemytrip.com/")
        self.assertIn("MakeMyTrip,", driver.title)
        time.sleep(10)
        all_menu = driver.find_element_by_class_name("arrow_downall")
        all_menu.send_keys(Keys.RETURN)
        time.sleep(10)
        way_field_radio = driver.find_element_by_xpath("//div/a/span[@class=\"radio_state\"]")
        way_field_radio.click()
        time.sleep(10)
        from_dest = driver.find_element_by_xpath("//*[@id=\"from_typeahead1\"]").click()
        from_dest.send_keys("Bhubaneshwar, India (BBI)")
        driver.find_element_by_xpath("//*[@id=\"to_typeahead1\"]").send_keys("New Delhi, India (DEL)")
        time.sleep(10)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
