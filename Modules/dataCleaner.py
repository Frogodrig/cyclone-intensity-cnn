# dataCleaning.py
#
# Purpose of this file:
# This file cleans and organizes the HURDAT2 
# best_track txt file acquired from: 
# https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2021-100522.txt
#
# A general Outline of this file:
# - Removes all whitespaces from the text file
# - Uses pandas to read and convert to a csv file
# - Correctly places data in their appropriate columns
# - When the script is finished, the best_track.csv file contains all relevant info about the cyclones


import pandas as pd
import numpy as np

# HURDAT2 best_track txt file path
txt_file_path = "C:/Users/Aditya Awasthi/Desktop/cyclone-intensity-cnn/besttrack.txt"


# Function to remove all whitespaces from the acquired txt file
def deleteWhiteSpaces(path): 

    # Reading from the file
    with open(path, 'r') as f:
        # Removing all spaces
        data = f.read().replace(' ', '')


    # Writing into the file
    with open(path, 'w') as f:
        f.write(data)


def cleanDatabase(path):

    # Calling the function to delete whitespaces
    deleteWhiteSpaces(path)


    # Reading the text file and separating data into their respective columns using "," as a separator
    df = pd.read_table(path, delimiter=',', names=["fulldate", "time", "col_3", "col_4", "lat_center", "lon_center", "max_sus_wind_speed", "col_8", "col_9", "col_10", "col_11", "col_12", "col_13", "col_14", "col_15", "col_16", "col_17", "col_18", "col_19", "col_20", "col_21"])


    # Dropping columns that are of no use to us
    df.drop(df.columns[[2, 3, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]], axis=1, inplace=True)


    # Organizing the cyclone_id and cyclone_name
    # Copying the "fulldate" column which contains data polluted with cyclone IDs and renaming the new column to "cyclone_id"
    df['cyclone_id'] = df['fulldate'].shift()
    # Copying the "time" column which contains data polluted with cyclone names and renaming the new column to "cyclone_name"
    df['cyclone_name'] = df['time'].shift()


    # Adding a year column
    # Using .apply() to "fulldate" column to perform some operation
    # Using the lambda function to perform list slicing to obtain the year
    df['year'] = df['fulldate'].apply(lambda x: x[:4])


    # Rearragning the columns to our liking
    df = df[['cyclone_id', 'cyclone_name', 'year', 'fulldate', 'time', 'lat_center', 'lon_center', 'max_sus_wind_speed']]


    # Dropping rows which have NULL (NaN) values
    df.dropna(inplace=True)


    # Temp variables to store data to be copied later
    temp_storm_id = ""
    temp_storm_name = ""


    # # Loop through all the indices of the df
    for index in df.index:
        # Check if the 1st character of the data begins with 'A'
        if (df["cyclone_id"][index][:1].isalpha()):
            temp_storm_id = df["cyclone_id"][index]

        else:
            df["cyclone_id"][index] = temp_storm_id


    # # Loop through all the indices of the df
    for index in df.index:
        if (df["cyclone_name"][index][:1].isalpha()):
            temp_storm_name = df["cyclone_name"][index]

        else:
            df["cyclone_name"][index] = temp_storm_name        


    # Save the cleaned data
    df.to_csv('C:/Users/Aditya Awasthi/Desktop/cyclone-intensity-cnn/besttrack.xlsx', index=False)


cleanDatabase(txt_file_path)