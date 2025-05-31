import selenium.webdriver as webdriver
from selenium.webdriver import ActionChains
from dotenv import load_dotenv
import os
import glob
from selenium.webdriver.common.keys import Keys
import time

def main():
    load_dotenv()
    csv_file = download_csv()
    if csv_file:
        print(f"CSV file downloaded successfully: {csv_file}")
    else:
        print("Failed to download CSV file.")

def download_csv(spreadsheet_url=None):
    driver = webdriver.Chrome()
    driver.get(spreadsheet_url)
    # Wait for the page to load
    time.sleep(3)  # Adjust the sleep time as necessary
    
    page_title = driver.title.split(" - ")[0].strip()  # Get the first part of the title
    print(f"Page title: {page_title}")
    
    
    # File > Download > csv
    # alt shift f
    ActionChains(driver).key_down(Keys.ALT).key_down(Keys.SHIFT).send_keys("f").key_up(Keys.SHIFT).key_up(Keys.ALT).perform()
    time.sleep(0.2)  # Adjust the wait time as necessary
    # d for download
    ActionChains(driver).send_keys("d").perform()
    time.sleep(0.2)  # Adjust the wait time as necessary
    # c for csv
    ActionChains(driver).send_keys("c").perform()
    # Wait for the download to complete
    time.sleep(2)  # Adjust the wait time as necessary
    driver.quit()

    # Get csv file
    csv_file = get_latest_csv_file()
    if csv_file:
        filename = os.path.basename(csv_file)
        if not filename.startswith(page_title):
            print(f"Warning: The downloaded file '{filename}' does not match the page title '{page_title}'.")
            return None
        else:
            print(f"CSV file downloaded: {csv_file}")
            #move to cwd
            if not os.path.exists("csv_snapshots"):
                os.makedirs("csv_snapshots")
            new_path = os.path.join(os.getcwd(), "csv_snapshots", page_title + time.strftime("-%Y%m%d-%H%M%S.csv"))
            os.rename(csv_file, new_path)
            return new_path

    else:
        print("No CSV file found.")
    return None
def get_latest_csv_file():
    downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    csv_files = glob.glob(os.path.join(downloads_folder, "*.csv"))
    if not csv_files:
        return None
    latest_file = max(csv_files, key=os.path.getctime)
    return latest_file
if __name__ == "__main__":
    main()