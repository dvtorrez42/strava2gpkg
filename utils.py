import os
import re
import zipfile

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

        
def gpx_to_gdf(gpx_files):
    """Creates a geodataframe from a list of .gpx files"""
    
    gdf_list = []

    for file_path in gpx_files:
        if file_path.endswith(('.gpx')):
            file_name_clean = (re.sub(r"\.gpx$", "", file_path))
            #print(file_name_clean)
            try:
                gdf = gpd.read_file(file_path, layer='tracks')
                if gdf.shape[0]>0:
                    gdf = gdf[['name', 'type', 'geometry']]
                    gdf['id'] = file_name_clean.lstrip('./activities')
                    gdf = gdf.set_index('id')
                    gdf_list.append(gdf)
            except:
                print("Error", file_path)

    gdf_all = pd.concat(gdf_list, ignore_index=False)
    return gdf_all


def read_activities(activities_file_path):  # TODO: parse dates
    activities_cols = [
        'Nombre de archivo',
        'Fecha de la actividad',
        'Tipo de actividad',
        'Tiempo transcurrido',
        'Distancia',
        'Ritmo cardíaco máx.',
        'Esfuerzo relativo',
        'Tiempo transcurrido.1',
        'Tiempo en movimiento',
        'Distancia.1',
        'Velocidad máxima',
        'Velocidad promedio',
        'Desnivel positivo',
        'Desnivel negativo',
        'Ritmo cardíaco promedio',
        'Calorías',
        'Esfuerzo relativo.1',
        'Condición climática',
        'Temperatura',
        'Sensación térmica',
        'Presión atmosférica',
        'Velocidad del viento',
        'Hora de salida del sol',
        'Hora de puesta del sol',
        'Fase lunar',
        'Nubosidad',
        'Índice UV',
        'Velocidad promedio durante el tiempo transcurrido',
        'Pasos en total'
    ]
    
    # Read the first few rows of the file to identify the available columns
    available_columns = pd.read_csv(activities_file_path, nrows=0).columns

    # Filter out columns that are not in the file
    valid_columns = [col for col in activities_cols if col in available_columns]
    
    activities = pd.read_csv(activities_file_path, usecols=valid_columns, parse_dates=False)  # TODO:parse dates , index_col='Nombre de archivo'
    activities['Nombre de archivo'] = activities['Nombre de archivo'].map(lambda x: x.lstrip('activities/').rstrip('gpx').rstrip('.fit.gz'))
    activities = activities.set_index('Nombre de archivo')
    activities.index.names = ['id']
    return activities

def split_dataframe_by_column(df, column_name):
    
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' does not exist if the DataFrame.")
    
    # Group the DataFrame by the specified column and converto to dictionay
    dataframes = {value: group for value, group in df.groupby(colum_name)}
    
    return dataframes