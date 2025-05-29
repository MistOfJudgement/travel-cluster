
import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys

def get_coordinates(address):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps")
    time.sleep(1)  # Wait for the page to load
    search_box = driver.find_element("name", "q")
    search_box.send_keys(address)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2.5)  # Wait for the results to load
    try:
        # Get the coordinates from the URL
        url = driver.current_url
        if "@" in url:
            coords = url.split("@")[1].split(",")
            latitude = coords[0]
            longitude = coords[1].split(",")[0]
            print(f"Coordinates for '{address}': {latitude}, {longitude}")
            return latitude, longitude
        else:
            print(f"Could not find coordinates for '{address}'.")
            return None
    except Exception as e:
        print(f"Error retrieving coordinates: {e}")
        return None
    finally:
        driver.quit()
        
if __name__ == "__main__":
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    coords = get_coordinates(address)
    if coords:
        print(f"Coordinates: {coords[0]}, {coords[1]}")
    else:
        print("Failed to retrieve coordinates.")
        