import os
import re
import zipfile
from datetime import datetime

import pandas as pd
import geopandas as gpd


def get_zip_file(directory):
    zip_files = [file for file in os.listdir(directory) if file.endswith('.zip')]

    if len(zip_files) == 1:
        return os.path.join(directory, zip_files[0])
    elif len(zip_files) > 1:
        print("There is more than one .zip file in the directory.")
        # Handle the case when there are multiple .zip files
    else:
        print("No .zip file found in the directory.")
        # Handle the case when there are no .zip files


def extract_desired_files(zip_file_path, destination_path, starts_with):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.startswith(starts_with):
                zip_ref.extract(file, destination_path)
    return print(f"Extraction complete. Files are in: {destination_path}")


def gpx_to_gdf(file_paths):
    """Creates a geodataframe from a list of .gpx files"""
    
    gdf_list = []

    for file_path in file_paths:
        if file_path.endswith(('.gpx')):
            file_name_clean = (re.sub(r"\.gpx$", "", file_path))
            #print(file_name_clean)
            try:
                gdf = gpd.read_file(file_path, layer='tracks')
                if gdf.shape[0]>0:
                    file_name_clean = re.sub(r"\.gpx$", "", file_path)
                    gdf['id_track'] = file_name_clean
                    gdf_list.append(gdf)
            except:
                print("Error", file)
    
    gdf_all = pd.concat(gdf_list, ignore_index=True)
    return gdf_all
                

def main():
    directory_path = './'
    zip_file_path = get_zip_file(directory_path)

    destination_path = './data/'
    starts_with = 'activities'
    extract_desired_files(zip_file_path=zip_file_path,
                         destination_path=destination_path,
                         starts_with=starts_with)

    gpx_directory = destination_path+"activities/"
    gpx_files = [os.path.join(gpx_directory, file) for file in os.listdir(gpx_directory) if file.endswith('.gpx')]

    strava_gdf = gpx_to_gdf(gpx_files)
    strava_gdf.to_file(f"./strava_{datetime.today().strftime('%Y-%m-%d')}.gpkg", 
                        driver='GPKG', 
                        layer=f"bike_{datetime.today().strftime('%Y-%m-%d')}")
    
    
if __name__ == "__main__":
    main()