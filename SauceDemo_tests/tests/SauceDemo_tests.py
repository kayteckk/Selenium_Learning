
#ARCHAIC, DO NOT USE -- JUST FOR REFRENCE TO SEE PROGRESS

import selenium
import selenium.webdriver as webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
from test_utils import login, add_to_cart
import pytest


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(1)
    yield driver
    driver.quit()


def test_login_logout(driver):
    login(driver,"https://www.saucedemo.com/","standard_user","secret_sauce")
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    burger_menu = driver.find_element(By.ID, "react-burger-menu-btn")
    burger_menu.click()
    logout_button = driver.find_element(By.ID, "logout_sidebar_link")
    driver.implicitly_wait(1)
    logout_button.click()
    assert driver.current_url == "https://www.saucedemo.com/"


def test_wrong_credentials(driver):
    login(driver,"https://www.saucedemo.com/","wrong","wrong2")
    error_button = driver.find_element(By.CLASS_NAME, "error-button")
    assert error_button.is_displayed()

def test_add_to_cart(driver):
    add_to_cart(driver)
    badge_item_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge_item_count.text == "1"

def test_remove_from_cart(driver):
    add_to_cart(driver)
    badge_item_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    badge_item_count.click()
    assert driver.current_url == ("https://www.saucedemo.com/cart.html")
    remove_from_cart_button = driver.find_element(By.ID, "remove-sauce-labs-backpack")
    remove_from_cart_button.click()
    removed_cart_item = driver.find_element(By.CLASS_NAME,"removed_cart_item")
    assert removed_cart_item.is_enabled()

    
def test_sorting_asc(driver):
    login(driver,"https://www.saucedemo.com/","standard_user","secret_sauce")
    select_by_price_asc = Select(driver.find_element(By.CLASS_NAME,"product_sort_container"))
    select_by_price_asc.select_by_value("lohi")
    product_prices = driver.find_elements(By.CLASS_NAME,"inventory_item_price")
    assert product_prices[0].text == "$7.99"

def test_sorting_desc(driver):
    login(driver,"https://www.saucedemo.com/","standard_user","secret_sauce")
    select_by_price_desc = Select(driver.find_element(By.CLASS_NAME,"product_sort_container"))
    select_by_price_desc.select_by_value("hilo")
    product_prices = driver.find_elements(By.CLASS_NAME,"inventory_item_price")
    assert product_prices[0].text == "$49.99"
    
def test_description(driver):
    login(driver,"https://www.saucedemo.com/","standard_user","secret_sauce")
    select_bikelight = driver.find_element(By.XPATH,"//*[@id='item_0_title_link']/div")
    select_bikelight.click()
    description = driver.find_element(By.CLASS_NAME,"inventory_details_desc")
    assert description.text == "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included."

def test_checkout(driver):
    login(driver,"https://www.saucedemo.com/","standard_user","secret_sauce")
    add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart_button.click()
    shopping_cart_link = driver.find_element(By.CLASS_NAME,"shopping_cart_link")
    shopping_cart_link.click()
    assert driver.current_url == "https://www.saucedemo.com/cart.html"
    checkout_button = driver.find_element(By.ID,"checkout")
    checkout_button.click()
    fName = driver.find_element(By.ID,"first-name")
    lName = driver.find_element(By.ID,"last-name")
    zipCode = driver.find_elements(By.ID,"postal-code")
    continue_button = driver.find_element(By.ID,"continue")
    fName.send_keys("John")
    lName.send_keys("Doe")
    zipCode[0].send_keys("12345")
    entered_zip = zipCode[0].get_attribute("value")
    assert len(entered_zip) == 5
    assert entered_zip.isdigit()
    continue_button.click()
    finish = driver.find_element(By.ID,"finish")
    finish.click()
    assert driver.current_url == "https://www.saucedemo.com/checkout-complete.html"

def test_sql_injection(driver):
    login(driver,"https://www.saucedemo.com/","' OR '1'='1","' OR '1'='1")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    error_button = driver.find_element(By.CLASS_NAME, "error-button")
    assert error_button.is_displayed()
    error_button.click()
    login(driver,"https://www.saucedemo.com/","' UNION SELECT 'username', 'password' FROM 'users' --","")
    error_button = driver.find_element(By.CLASS_NAME, "error-button")
    assert error_button.is_displayed()
    error_button.click()
    login(driver,"https://www.saucedemo.com/","admin' --","")
    error_button = driver.find_element(By.CLASS_NAME, "error-button")
    assert error_button.is_displayed()
