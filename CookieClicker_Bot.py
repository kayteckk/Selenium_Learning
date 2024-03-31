import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
import time
from pynput import keyboard
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBot():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.driver.implicitly_wait(2)
        consent = self.driver.find_element(By.CLASS_NAME,"fc-button")
        consent.click()
        langSelect = self.driver.find_element(By.CLASS_NAME,"langSelectButton")
        langSelect.click()
        self.running = True
        self.cookie = self.driver.find_element(By.ID, "bigCookie")
        self.timer = 0

    def focus_window(self):
        self.driver.execute_script("window.focus();")

    def click_cookie(self):
        self.focus_window()
        try:
            self.cookie = self.driver.find_element(By.ID, "bigCookie")
            self.cookie.click()
        except Exception as e:
            print(f"Error in click_cookie: {e}")

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('q'):
            print("Zatrzymywanie bota...")
            self.running = False

    def start_listening(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def buy_store_upgrade(self):
        try:
            store_upgrade = self.driver.find_element(By.ID,"upgrade0")
            if store_upgrade.is_displayed() and store_upgrade.is_enabled():
                store_upgrade.click()
        except Exception as e:
            print(f"Error in buy_store_upgrade: {e}")



    def buy_items(self):
        try:
            items = self.driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
            for item in items[::-1]:
                try:
                    item_id = item.get_attribute('id')
                    refreshed_item = self.driver.find_element(By.ID, item_id)
                    if refreshed_item.is_displayed() and refreshed_item.is_enabled():
                        refreshed_item.click()
                except Exception as e:
                    print(f"Error while clicking an item in buy_items: {e}")
        except Exception as e:
            print(f"Error in buy_items: {e}")


    def main(self):
        self.start_listening()
        while self.running:
            self.click_cookie()
            if self.timer > 3:
                self.buy_store_upgrade()
                self.buy_items()
                self.timer = 0
            self.timer += 0.05
            self.focus_window()
            time.sleep(0.05)
        print("Bot was stopped.")
        self.driver.quit()


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.main()
