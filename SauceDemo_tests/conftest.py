import pytest
from selenium.webdriver import Chrome

@pytest.fixture(scope="function")
def driver():
    driver = Chrome()
    yield driver
    driver.quit()
