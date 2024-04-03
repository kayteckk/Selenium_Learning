from selenium.webdriver.common.by import By
import pytest

def login(driver, url, username, password):
    driver.get(url)
    login_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_field.send_keys(username)
    password_field.send_keys(password)
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

def add_to_cart(driver):
    login(driver, "https://www.saucedemo.com/", "standard_user", "secret_sauce")
    add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_to_cart_button.click()
