import os
from datetime import datetime

import pandas as pd
import geopandas as gpd

from utils import (
    get_zip_file, 
    extract_desired_files,
    gpx_to_gdf,
    read_activities
)
                
directory_path = './'  # '../usr/local/strava/'
destination_path = './'  # '../usr/local/strava/data/'
gpx_directory = destination_path+"activities/"

def main():
    zip_file_path = get_zip_file(directory_path)
    extract_desired_files(
        zip_file_path=zip_file_path,
        destination_path=destination_path,
        starts_with='activities'
        )

    gpx_files = [os.path.join(gpx_directory, file) for file in os.listdir(gpx_directory) if file.endswith('.gpx')]

    strava_gdf = gpx_to_gdf(gpx_files)
    strava_gdf.to_file(
        f"../usr/local/strava/strava_{datetime.today().strftime('%Y-%m-%d')}.gpkg",# f"../usr/local/strava/strava_{datetime.today().strftime('%Y-%m-%d')}.gpkg", 
        driver='GPKG', 
        layer=f"bike_{datetime.today().strftime('%Y-%m-%d')}"
        )

if __name__ == "__main__":
    main()