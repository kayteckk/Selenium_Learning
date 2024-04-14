from selenium.webdriver.common.by import By

class ProductDetailsPage:
    DESCRIPTION = (By.CLASS_NAME, "inventory_details_desc")
    

    def __init__(self, driver):
        self.driver = driver

    def get_description_text(self):
        return self.driver.find_element(*self.DESCRIPTION).text