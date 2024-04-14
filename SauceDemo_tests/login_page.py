from selenium.webdriver.common.by import By

class LoginPage:
    URL = "https://www.saucedemo.com/"
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_BUTTON = (By.CLASS_NAME,"error-button")

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def error_button_is_shown(self):
        return self.driver.find_element(*self.ERROR_BUTTON).is_displayed()

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()
