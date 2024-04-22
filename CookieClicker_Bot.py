import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
import time
import json

class SeleniumBot():
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--user-data-dir=/Users/kajetankotarski/Library/Application Support/Google/Chrome/Profile 1') # <---- your path to Chrome should go here
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get("https://orteil.dashnet.org/cookieclicker/")
        self.load_local_storage()
        self.wait = WebDriverWait(self.driver, 2)
        self.running = True
        self.cookie = self.wait.until(EC.visibility_of_element_located((By.ID, "bigCookie")))
        self.timer = 0

    def save_local_storage(self, path="local_storage.json"):
        local_storage = self.driver.execute_script("return window.localStorage;")
        with open(path, "w") as file:
            json.dump(local_storage, file)

    def load_local_storage(self, path="local_storage.json"):
        try:
            with open(path, "r") as file:
                local_storage = json.load(file)
            for key, value in local_storage.items():
                self.driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        except FileNotFoundError:
            print("No local storage found")

    def focus_window(self):
        self.driver.execute_script("window.focus();")

    def click_cookie(self):
        self.focus_window()
        self.cookie.click()

    def on_press(self, key):
        if key == keyboard.KeyCode.from_char('q'):
            print("Stopping the bot...")
            self.running = False

    def start_listening(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()

    def buy_store_upgrade(self):
        try:
            store_upgrade = self.wait.until(EC.visibility_of_element_located((By.ID, "upgrade0")))
            store_upgrade.click()
        except:
            Print("Not enough cookies.")

    def buy_items(self):
        try:
            items = self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".product.unlocked.enabled")))
            for item in items[::-1]:
                item_id = item.get_attribute('id')
                refreshed_item = self.wait.until(EC.visibility_of_element_located((By.ID, item_id)))
                refreshed_item.click()
        except:
            print("Not enough cookies.")

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
        self.save_local_storage()
        time.sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    bot = SeleniumBot()
    bot.main()
