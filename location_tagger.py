import geocoder
import glob
import os
import csv
def main():
    csv_filepath = get_latest_csv_filepath()
    data = []
    headers = []
    with open(csv_filepath, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            data.append(row)
         
    address_col = headers.index("Address") if "Address" in headers else None
    latitude_col = headers.index("Latitude") if "Latitude" in headers else None
    longitude_col = headers.index("Longitude") if "Longitude" in headers else None
    edits = [] 
    if address_col is None or latitude_col is None or longitude_col is None:
        print("CSV file does not contain required columns: Address, Latitude, Longitude")
        return
    for i, row in enumerate(data):
        #if missing address, skip
        if not row[address_col]:
            continue
        # if contains latitude and longitude, skip
        if row[latitude_col] and row[longitude_col]:
            continue
        # geocode
        address = row[address_col]
        print(f"Geocoding address: {address}")
        lat, long = geocoder.get_coordinates(address)
        if lat is not None and long is not None:
            row[latitude_col] = lat
            edits.append((i, latitude_col, lat))
            row[longitude_col] = long
            edits.append((i, longitude_col, long))
            print(f"Updated row with latitude: {lat}, longitude: {long}")
            
        else:
            print(f"Failed to geocode address: {address}")
    print("Geocoding completed. Edits made:")
    for edit in edits:
        print(f"Row {edit[0]}, Column {edit[1]}: {edit[2]}")
def get_latest_csv_filepath():
    folder = os.path.join(os.getcwd(), "csv_snapshots")
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        return None
    latest_file = max(csv_files, key=os.path.getctime)
    return latest_file
if __name__ == "__main__":
    main()