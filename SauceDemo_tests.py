import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import unittest
import time

class SeleniumTest(unittest.TestCase):
    URL = "https://www.saucedemo.com/"

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get(self.URL)
        login_field = self.driver.find_element(By.ID, "user-name")
        password_field = self.driver.find_element(By.ID, "password")
        login_field.send_keys(username)
        password_field.send_keys(password)
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
    
    def test_login(self):
        self.login("standard_user","secret_sauce")
        self.assertEqual(self.driver.current_url,"https://www.saucedemo.com/inventory.html")

    def test_sauce_demo_login_logout(self):
        self.login("standard_user", "secret_sauce")
        self.assertEqual(self.driver.current_url, "https://www.saucedemo.com/inventory.html")
        burger_menu = self.driver.find_element(By.ID, "react-burger-menu-btn")
        burger_menu.click()
        logout_button = self.driver.find_element(By.ID, "logout_sidebar_link")
        logout_button.click()
        self.assertEqual(self.driver.current_url, self.URL)

    def test_wrong_credentials(self):
        self.login("wrong", "wrong2")
        error_button = self.driver.find_element(By.CLASS_NAME, "error-button")
        self.assertTrue(error_button.is_displayed())
    
    def add_to_cart(self):
        self.login("standard_user", "secret_sauce")
        add_to_cart_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()

    def test_add_to_cart(self):
        self.login("standard_user", "secret_sauce")
        add_to_cart_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()
        badge_item_count = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        self.assertEqual(badge_item_count.text, "1")
    
    def test_remove_from_cart(self):
        self.login("standard_user", "secret_sauce")
        self.add_to_cart()
        badge_item_count = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        badge_item_count.click()
        self.assertEqual(self.driver.current_url,"https://www.saucedemo.com/cart.html")
        remove_from_cart_button = self.driver.find_element(By.ID, "remove-sauce-labs-backpack")
        remove_from_cart_button.click()
        removed_cart_item = self.driver.find_element(By.CLASS_NAME,"removed_cart_item")
        self.assertEqual(removed_cart_item.is_enabled(), True)
    
    def test_sorting_asc(self):
        self.login("standard_user", "secret_sauce")
        select_by_price_asc = Select(self.driver.find_element(By.CLASS_NAME,"product_sort_container"))
        select_by_price_asc.select_by_value("lohi")
        product_prices = self.driver.find_elements(By.CLASS_NAME,"inventory_item_price")
        self.assertEqual(product_prices[0].text, "$7.99")
    
    def test_sorting_desc(self):
        self.login("standard_user", "secret_sauce")
        select_by_price_desc = Select(self.driver.find_element(By.CLASS_NAME,"product_sort_container"))
        select_by_price_desc.select_by_value("hilo")
        product_prices = self.driver.find_elements(By.CLASS_NAME,"inventory_item_price")
        self.assertEqual(product_prices[0].text, "$49.99")
    
    def test_description(self):
        self.login("standard_user","secret_sauce")
        select_bikelight = self.driver.find_element(By.XPATH,"//*[@id='item_0_title_link']/div")
        select_bikelight.click()
        description = self.driver.find_element(By.CLASS_NAME,"inventory_details_desc")
        self.assertEqual(description.text,"A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.")

    def test_checkout(self):
        self.login("standard_user","secret_sauce")
        add_to_cart_button = self.driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        add_to_cart_button.click()
        shopping_cart_link = self.driver.find_element(By.CLASS_NAME,"shopping_cart_link")
        shopping_cart_link.click()
        self.assertEqual(self.driver.current_url,"https://www.saucedemo.com/cart.html")
        checkout_button = self.driver.find_element(By.ID,"checkout")
        checkout_button.click()
        fName = self.driver.find_element(By.ID,"first-name")
        lName = self.driver.find_element(By.ID,"last-name")
        zipCode = self.driver.find_elements(By.ID,"postal-code")
        continue_button = self.driver.find_element(By.ID,"continue")
        fName.send_keys("John")
        lName.send_keys("Doe")
        zipCode[0].send_keys("12345")
        entered_zip = zipCode[0].get_attribute("value")
        self.assertEqual(len(entered_zip), 5)
        self.assertTrue(entered_zip.isdigit())
        continue_button.click()
        finish = self.driver.find_element(By.ID,"finish")
        finish.click()
        self.assertEqual(self.driver.current_url,"https://www.saucedemo.com/checkout-complete.html")

    
    def test_sql_injection(self):
        self.login("' OR '1'='1","' OR '1'='1")
        login_button = self.driver.find_element(By.ID, "login-button")
        login_button.click()
        error_button = self.driver.find_element(By.CLASS_NAME, "error-button")
        self.assertTrue(error_button.is_displayed())
        self.login("' UNION SELECT 'username', 'password' FROM 'users' --","")
        error_button = self.driver.find_element(By.CLASS_NAME, "error-button")
        self.assertTrue(error_button.is_displayed())
        self.login("admin' --","")
        error_button = self.driver.find_element(By.CLASS_NAME, "error-button")
        self.assertTrue(error_button.is_displayed())


if __name__ == "__main__":
    unittest.main()
