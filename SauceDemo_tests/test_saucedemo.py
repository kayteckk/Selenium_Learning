import pytest
from selenium.webdriver import Chrome
from .login_page import LoginPage
from .product_page import ProductPage
from selenium.webdriver.common.by import By
from .product_details_page import ProductDetailsPage
from .shopping_cart_page import ShoppingCartPage
from .checkout_page import CheckoutPage

@pytest.fixture(scope="function")
def driver():
    driver = Chrome()
    driver.implicitly_wait(1)
    yield driver
    driver.quit()

def test_login_logout(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    login_page.load()
    login_page.login("standard_user", "secret_sauce")
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    
    product_page.logout()
    assert driver.current_url == "https://www.saucedemo.com/"

def test_wrong_login(driver):
    login_page = LoginPage(driver)
    login_page.load()
    login_page.login("wrong_user", "secret_sauce")
    
    assert login_page.error_button_is_shown()

def test_add_item_to_cart(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.add_to_cart()

    assert product_page.get_shopping_cart_count() == "1" 

def test_remove_from_cart(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    shopping_cart_page = ShoppingCartPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.add_to_cart()
    assert product_page.get_shopping_cart_count() == "1"
    shopping_cart_page.go_to_cart()
    assert shopping_cart_page.remove_from_cart() == True

def test_sorting_asc(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.sort_products_by("lohi")
    assert product_page.get_min_product_price() == "$7.99"

def test_sorting_desc(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.sort_products_by("hilo")
    assert product_page.get_min_product_price() == "$49.99"

def test_description(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    product_details_page = ProductDetailsPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.select_product_and_go_to_details()  # Wybieramy pierwszy produkt i przechodzimy do jego szczegółów

    description_text = product_details_page.get_description_text()

    assert description_text == "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included."

def test_checkout(driver):
    login_page = LoginPage(driver)
    product_page = ProductPage(driver)
    shopping_cart_page = ShoppingCartPage(driver)
    checkout_page = CheckoutPage(driver)

    login_page.load()
    login_page.login("standard_user", "secret_sauce")

    product_page.add_to_cart()
    shopping_cart_page.go_to_cart()

    shopping_cart_page.go_to_checkout()

    checkout_page.fill_checkout_form("John", "Doe", "12345")

    assert checkout_page.is_zip_code_valid()

    checkout_page.click_finish()

    assert driver.current_url == "https://www.saucedemo.com/checkout-complete.html"

def test_sql_injection(driver):
    login_page = LoginPage(driver)
    login_page.load()


    login_page.login("' OR '1'='1", "' OR '1'='1")
    assert login_page.error_button_is_shown()

    login_page.login("' UNION SELECT 'username', 'password' FROM 'users' --", "")
    assert login_page.error_button_is_shown()

    login_page.login("admin' --", "")
    assert login_page.error_button_is_shown()