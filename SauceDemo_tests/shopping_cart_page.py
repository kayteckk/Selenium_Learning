from selenium.webdriver.common.by import By


class ShoppingCartPage:
    CHECKOUT_BUTTON = (By.ID, "checkout")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    REMOVE_FROM_CART = (By.ID, "remove-sauce-labs-backpack")
    EMPTY_CART_ITEM = (By.CLASS_NAME,"removed_cart_item")
    
    def __init__(self, driver):
        self.driver = driver

    def go_to_cart(self):
        self.driver.find_element(*self.SHOPPING_CART_BADGE).click()

    def remove_from_cart(self):
        self.driver.find_element(*self.REMOVE_FROM_CART).click()
        return self.driver.find_element(*self.EMPTY_CART_ITEM).is_enabled()

    def go_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()

