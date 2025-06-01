
import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def get_coordinates(address):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps")
    time.sleep(1)  # Wait for the page to load
    search_box = driver.find_element("name", "q")
    search_box.send_keys(address)
    # sibling element is the list of suggestions
    driver.implicitly_wait(3)
    #<div data-index="0" jsaction="suggestion.select"><div class="ZHeE1b " jslog="6986;mutable:true;"><div class="l0wghb " role="row"><div class="DgCNMb " id="cell0x0" role="gridcell"><div class="jlzIOd"><span class="google-symbols" aria-hidden="true" style="font-size: 21px;"></span></div><span></span><span class="cGyruf fontBodyMedium RYaupb "><span>諏訪神社本殿</span></span><div class="OyjIsf "></div> <span class="EmLCAe fontBodyMedium"><span>Japan, Kanagawa, Yokosuka, </span><span class="XYuRPe">Midorigaoka, 34</span></span></div></div></div></div>
    suggestions = driver.find_elements("css selector", 'div[jsaction="suggestion.select"]')
    if suggestions:
        # Click the first suggestion
        suggestions[0].click()
    else:
        print(f"No suggestions found for '{address}'.")
        driver.quit()
        return None 
    time.sleep(2.5)  # Wait for the results to load
    # time.sleep(10)
    try:
        # Get the coordinates from the URL
        url = driver.current_url
        if "@" in url:
            coords = url.split("@")[1].split(",")
            latitude = coords[0]
            longitude = coords[1].split(",")[0]
            driver.implicitly_wait(3)
            time.sleep(1)  # Wait for the address to be displayed

            clean_address = driver.find_element(By.CSS_SELECTOR, '[data-tooltip="Copy address"]').get_attribute("aria-label").split("Address: ")[-1] 
            # clean_address = driver.find_element(By.XPATH, "//[@data-item-id='address']").get_attribute("aria-label").split("Address, ")[-1]
            print(f"Coordinates for '{address}': {latitude}, {longitude}")
            return latitude, longitude, clean_address
        else:
            print(f"Could not find coordinates for '{address}'.")
            return None
    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None
    finally:
        driver.quit()
        
if __name__ == "__main__":
    address = "34 Midorigaoka, Yokosuka, Kanagawa 238-0018, Japan"
    coords = get_coordinates(address)
    if coords:
        print(f"Coordinates: {coords[0]}, {coords[1]}")
    else:
        print("Failed to retrieve coordinates.")
