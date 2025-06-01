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
        self.row = 0
        self.col = 0

    def open_spreadsheet(self, url):
        self.driver.get(url)
        time.sleep(2)  # Wait for the page to load

    def close_spreadsheet(self):
        self.driver.quit()

    def navigate_to_cell(self, col, row):
        row_offset = row - self.row
        col_offset = col - self.col
        self.row = row
        self.col = col
        delay = 0.1
        to_send = []
        if row_offset > 0:
            for _ in range(row_offset):
                to_send.append(Keys.ARROW_DOWN)
        elif row_offset < 0:
            for _ in range(-row_offset):
                to_send.append(Keys.ARROW_UP)
        if col_offset > 0:
            for _ in range(col_offset):
                to_send.append(Keys.ARROW_RIGHT)
        elif col_offset < 0:
            for _ in range(-col_offset):
                to_send.append(Keys.ARROW_LEFT)
        for key in to_send:
            self.actions.send_keys(key)
            self.actions.perform()
            time.sleep(delay)
    def reset_loc(self):
       self.shortcut([Keys.CONTROL, Keys.HOME])
       self.col = 0
       self.row = 0 
    def shortcut(self, keys):
        modifiers = keys[:-1]
        key = keys[-1]
        for modifier in modifiers:
            self.actions.key_down(modifier)
        self.actions.send_keys(key)
        for modifier in modifiers:
            self.actions.key_up(modifier)
        self.actions.perform()
        time.sleep(0.1)

    def put_text(self, text):
        self.actions.send_keys(text)
        self.actions.send_keys(Keys.ENTER)
        self.row += 1
        self.actions.perform()
        time.sleep(0.1)  # Wait for the text to be entered
    
if __name__ == "__main__":
    load_dotenv()
    url = os.getenv("TEST_SPREADSHEET_URL")
    controller = SpreadsheetController()
    controller.open_spreadsheet(url)
    time.sleep(2)  # Wait for the spreadsheet to load
    controller.navigate_to_cell(2, 0)  # Navigate to cell (2, 0)
    controller.put_text("Hello, World!")  # Put text in the cell
    controller.navigate_to_cell(3, 0)  # Navigate to cell (3, 0)
    controller.put_text("This is a test.")  # Put text in the next cell
    controller.navigate_to_cell(1, 2)  # Navigate back to cell (1, 2)
    controller.put_text("Back to cell (1, 2)")  # Put text in cell (1, 2)
    # controller.shortcut([Keys.ALT, Keys.SHIFT, "f"])  # Example shortcut
    # time.sleep(2)  # Wait to see the effect of the shortcut
    # controller.close_spreadsheet()
    time.sleep(10)