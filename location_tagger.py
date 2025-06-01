import spreadsheet
from dotenv import load_dotenv
import geocoder
import glob
import os
import csv
import location_reader
from utils import get_latest_csv_filepath
class EditTracker:
    def __init__(self, headers, data):
        self.data = data
        self.headers = headers
        self.edits = []

    def add_edit(self, row, col, value):
        self.edits.append((row, col, value))

    def get_edits(self):
        return self.edits

    def get_data(self):
        return self.data

    def get_headers(self):
        return self.headers

    def get_value(self, row, col):
        if row < len(self.data) and col < len(self.headers):
            return self.data[row][col]
        return None

    def set_value(self, row, col, value):
        if isinstance(col, str):
            col = self.col_index(col)
        if row < len(self.data) and col < len(self.headers):
            if self.get_value(row, col) == value:
                return
            self.data[row][col] = value
            self.add_edit(row+1, col, value)
        else:
            raise IndexError("Row or column index out of range.")

    def col_index(self, col_name):
        if col_name in self.headers:
            return self.headers.index(col_name)
        else:
            raise ValueError(f"Column '{col_name}' not found in headers.")

def read_csv_file(csv_filepath):
    data = []
    headers = []
    with open(csv_filepath, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            data.append(row)
    return headers, data 

def load_data(file_provider) -> EditTracker:
    file = file_provider()
    headers, file_data = read_csv_file(file)
    return EditTracker(headers, file_data)

def tag_locations(data_tracker, geocoder_service):
    for i, row in enumerate(data_tracker.get_data()):
        if row[data_tracker.col_index("Latitude")] and row[data_tracker.col_index("Longitude")]:
            continue

        address = row[data_tracker.col_index("Address")]
        if not address:
            if row[data_tracker.col_index("Place")].lower().startswith("any"):
                print(f"Skipping row {i+1} with empty address and 'Any' place.")
                continue
            address = row[data_tracker.col_index("Place")]
        print(f"Geocoding address: {address} (Row {i+1})")
        lat, long, clean_address = geocoder_service(address)
        if not lat or not long or not clean_address:
            print(f"Failed to geocode address: {address}")
            continue
        data_tracker.set_value(i, data_tracker.col_index("Latitude"), lat)
        data_tracker.set_value(i, data_tracker.col_index("Longitude"), long)
        data_tracker.set_value(i, data_tracker.col_index("Address"), clean_address)

mock_lat = 0.0
mock_long = 0.0
def mock_geocoder(address):
    global mock_lat, mock_long
    if not address:
        return None, None
    mock_lat += 0.1
    mock_long -= 0.1
    return mock_lat, mock_long
def mock_file_provider():
    return get_latest_csv_filepath("csv_snapshots")

def mock_apply_edits(tracker):
    for row, col, val in tracker.get_edits():
        print(f"Editing cell ({row}, {col}) with value: {val}")
def main():
    load_dotenv()
    url = os.getenv("SPREADSHEET_URL")

    tracker = load_data(file_provider=lambda : location_reader.download_csv(url))
    # tracker = load_data(file_provider=mock_file_provider)

    print(f"Loaded {len(tracker.get_data())} rows from the CSV file.")
    print(f"Headers: {tracker.get_headers()}")


    # tag_locations(tracker, geocoder_service=mock_geocoder)
    tag_locations(tracker, geocoder_service=geocoder.get_coordinates)

    # mock_apply_edits(tracker)
    apply_edits(tracker, url)  # Uncomment to apply edits to the spreadsheet


def apply_edits(tracker, url):
    # url = os.getenv("SPREADSHEET_URL")
    remote = spreadsheet.SpreadsheetController()
    remote.open_spreadsheet(url)
    
    import time
    for row, col, val in tracker.get_edits():
        print(f"Editing cell ({row}, {col}) with value: {val}")
        # remote.reset_loc()
        # time.sleep(0.1)
        remote.navigate_to_cell(col, row)
        time.sleep(0.1)  # Wait for the cell to be focused
        remote.put_text(str(val))
        time.sleep(0.1)  # Wait for the text to be entered

    time.sleep(7)  # Wait for the edits to be applied
    remote.close_spreadsheet()

if __name__ == "__main__":
    main()
    