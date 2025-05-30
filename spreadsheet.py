import selenium.webdriver as webdriver
from selenium.webdriver import ActionChains
from dotenv import load_dotenv
import os
import glob
from selenium.webdriver.common.keys import Keys
import time


class SpreadsheetController:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.actions = ActionChains(self.driver)
        load_dotenv()
        self.spreadsheet_url = os.getenv("SPREADSHEET_URL")
        self.row = 0
        self.col = 0

    def open_spreadsheet(self):
        self.driver.get(self.spreadsheet_url)

    def close_spreadsheet(self):
        self.driver.quit()

    def navigate_to_cell(self, col, row):
        row_offset = row - self.row
        col_offset = col - self.col
        if row_offset > 0:
            for _ in range(row_offset):
                self.actions.send_keys(Keys.ARROW_DOWN)
        elif row_offset < 0:
            for _ in range(-row_offset):
                self.actions.send_keys(Keys.ARROW_UP)
        if col_offset > 0:
            for _ in range(col_offset):
                self.actions.send_keys(Keys.ARROW_RIGHT)
        elif col_offset < 0:
            for _ in range(-col_offset):
                self.actions.send_keys(Keys.ARROW_LEFT)
        self.actions.perform()
    def shortcut(self, keys):
        modifiers = keys[:-1]
        key = keys[-1]
        for modifier in modifiers:
            self.actions.key_down(modifier)
        self.actions.send_keys(key)
        for modifier in modifiers:
            self.actions.key_up(modifier)
        self.actions.perform()
    def put_text(self, text):
        self.actions.send_keys(text)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()
    
if __name__ == "__main__":
    controller = SpreadsheetController()
    controller.open_spreadsheet()
    time.sleep(2)  # Wait for the spreadsheet to load
    controller.navigate_to_cell(2, 0)  # Navigate to cell (2, 0)
    # controller.shortcut([Keys.ALT, Keys.SHIFT, "f"])  # Example shortcut
    # time.sleep(2)  # Wait to see the effect of the shortcut
    # controller.close_spreadsheet()
    time.sleep(10)