from sklearn import cluster
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from utils import get_latest_csv_filepath
import location_reader
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    url = os.getenv("SPREADSHEET_URL")
    # Load the latest CSV file
    csv_file = location_reader.download_csv(url)
    # csv_file = get_latest_csv_filepath("csv_snapshots")
    if not csv_file:
        print("No CSV file found in 'csv_snapshots'.")
        return
    data = pd.read_csv(csv_file)
    # hierarchical clustering
    if 'Latitude' not in data.columns or 'Longitude' not in data.columns:
        print("CSV file must contain 'Latitude' and 'Longitude' columns.")
        return
    
    data = data.dropna(subset=['Latitude', 'Longitude'])
    coords = data[['Latitude', 'Longitude']].values
    print(f"Using {len(coords)} valid coordinates for clustering.")
    # Perform clustering
    clustering = cluster.AgglomerativeClustering(n_clusters=5)
    clustering.fit(coords)
    # Add cluster labels to the DataFrame
    
    data['Cluster'] = clustering.labels_
    
    #plot coordinates with cluster labels
    plt.figure(figsize=(10, 6))
    plt.scatter(data['Longitude'], data['Latitude'], c=data['Cluster'], cmap='viridis', marker='o')
    plt.title('Hierarchical Clustering of Locations')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.colorbar(label='Cluster')
    plt.show()


if __name__ == "__main__": main()
