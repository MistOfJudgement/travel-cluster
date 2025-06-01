from sklearn import cluster
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from utils import get_latest_csv_filepath
import location_reader
import os
from dotenv import load_dotenv
import smopy
def main():

    load_dotenv()
    url = os.getenv("SPREADSHEET_URL")
    # Load the latest CSV file
    # csv_file = location_reader.download_csv(url)
    csv_file = get_latest_csv_filepath("csv_snapshots")
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
   
    bounds = data[['Latitude', 'Longitude']].agg(['min', 'max'])
    map = smopy.Map(bounds['Latitude']['min'], bounds['Longitude']['min'],
                    bounds['Latitude']['max'], bounds['Longitude']['max'],
                    z=12)
    fig, ax = plt.subplots(figsize=(10, 10))
    map.show_mpl(ax=ax)
    # Plot the clusters
    for cluster_id in np.unique(data['Cluster']):
        cluster_data = data[data['Cluster'] == cluster_id]
        x, y = map.to_pixels(cluster_data['Latitude'].values, cluster_data['Longitude'].values)
        ax.scatter(x, y, label=f'Cluster {cluster_id}', alpha=0.6)
    # Plot the original locations
    
    ax.set_title('Hierarchical Clustering of Locations')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.legend()
    plt.show()
    
if __name__ == "__main__": main()
