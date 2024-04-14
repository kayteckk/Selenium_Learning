from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class ProductPage:
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ADD_TO_CART_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    REMOVE_FROM_CART = (By.ID, "remove-sauce-labs-backpack")
    EMPTY_CART_ITEM = (By.CLASS_NAME,"removed_cart_item")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    PRODUCT_PRICES = (By.CLASS_NAME,"inventory_item_price")

    def __init__(self, driver):
        self.driver = driver
    

    def sort_products_by(self, order):
        select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        select.select_by_value(order)
    
    def get_min_product_price(self):
        PRODUCT_PRICES = self.driver.find_elements(*self.PRODUCT_PRICES)

        return PRODUCT_PRICES[0].text


    def get_shopping_cart_count(self):
        return self.driver.find_element(*self.SHOPPING_CART_BADGE).text


    
    def select_product_and_go_to_details(self):
        product_link = self.driver.find_element(By.XPATH,"//*[@id='item_0_title_link']/div")
        product_link.click()

    def logout(self):
        self.driver.find_element(*self.BURGER_MENU).click()
        self.driver.implicitly_wait(1)
        self.driver.find_element(*self.LOGOUT_LINK).click()

    def add_to_cart(self):
        self.driver.find_element(*self.ADD_TO_CART_BUTTON).click()
