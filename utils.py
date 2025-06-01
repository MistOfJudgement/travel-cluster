import os
import glob

def get_latest_csv_filepath(folder):
    if not os.path.isabs(folder):
        folder = os.path.join(os.getcwd(), folder)
    csv_files = glob.glob(os.path.join(folder, "*.csv"))
    if not csv_files:
        return None
    latest_file = max(csv_files, key=os.path.getctime)
    return latest_file

