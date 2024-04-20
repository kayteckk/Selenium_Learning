from selenium.webdriver.common.by import By

class CheckoutPage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    ZIP_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")

    def __init__(self, driver):
        self.driver = driver
        self.zipCode = ""

    def fill_checkout_form(self, first_name, last_name, zip_code):
        zip_code_elements = self.driver.find_elements(*self.ZIP_CODE_INPUT)
        zip_code_element = zip_code_elements[0]
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        zip_code_element.send_keys(zip_code)
        self.zipCode = zip_code
        self.driver.find_element(*self.CONTINUE_BUTTON).click()

    def click_finish(self):
        self.driver.find_element(*self.FINISH_BUTTON).click()
        
    def is_zip_code_valid(self):
        zipCode = self.zipCode
        return len(zipCode) == 5 and zipCode.isdigit()