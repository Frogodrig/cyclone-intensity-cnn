# labelling.py
#
# Purpose of this file:
# This file takes the satellite image files downloaded from download.py and turns them into NumPy arrays that will be
# fed to the neural network in Model/model.py
#
# A general outline of this file:
# - Crops each satellite image (64x64)
# - Matches each satellite image of a hurricane with the maximum sustained wind speed of that hurricane
# - Collects these images and their associated labels in arrays and saves them as numpy files


import pandas as pd
import numpy as np
import os
import netCDF4

# Reads in the Best Track dataset, which contain records of the location and maximum wind speed of every recorded
# hurricane in the Atlantic and Eastern/Central Pacific basins
best_track_data = pd.read_csv('besttrack.csv')

# The number of pixels wide and tall to crop the images of hurricanes to
side_length = 64

# Lists to hold the hurricane images and the wind speed associated with those images. These lists are aligned so that
# the first image in the images list corresponds to the first label in the labels list.
images = []
labels = []

# Gets list of names of files, each file containing a satellite image
files = os.listdir('Satellite Imagery')
num_files = len(files)

# Looping through each file in the directory
for i in range(num_files):
    # Get IR satellite image from the file
    raw_data = netCDF4.Dataset('Satellite Imagery/' + files[i])
    ir_data = raw_data.variables['IRWIN'][0]

    # Performing center cropping of the image
    x, y = ir_data.shape
    startx = x//2-(side_length//2)
    starty = y//2-(side_length//2)
    cropped_ir_data = ir_data[startx:startx+side_length,starty:starty+side_length]

    # Get storm name, date, and time of the hurricane from the image's file name
    file_name = files[i]
    file_name = file_name.split('.')
    storm_name = file_name[1]
    date = int(file_name[2] + file_name[3] + file_name[4])
    time = int(file_name[5])

    # Filter the best track dataset to find the row that matches the name, date, and time of this hurricane image
    matching_best_track_data = best_track_data.loc[
        (best_track_data.storm_name == storm_name) &
        (best_track_data.fulldate == date) &
        (best_track_data.time == time)
    ]

    # Get the wind speed from the row that matches the name, date, and time of this hurricane image
    try:
        wind_speed = matching_best_track_data.max_sus_wind_speed.reset_index(drop=True)[0]
    except Exception:
        print('\rCould not find label for image of ' + storm_name + ' at date ' + str(date) + ' and time ' + str(time), end='\n')
        continue  # Skip to the next hurricane image if the a wind speed could not be found for this hurricane image

    # Add the image and wind speed to these lists. This way, the lists of images and labels always line up. The first
    # hurricane image in the images list is associated with the first wind speed in the labels list.
    images.append(cropped_ir_data)
    labels.append(wind_speed)

    raw_data.close()

    print('\rProcessing Samples... ' + str(round(((i + 1) / num_files) * 100, 1)) + '% (' + str(i + 1) + ' of ' + str(
        num_files) + ')', end='')

print('\nSaving NumPy arrays...')

# Turn the list of images and labels into NumPy arrays
images = np.array(images)
# print("-------------------------------------------------------------------")
# print("Shape of images array: ")
print(images.shape) #(4596, 64, 64)
# print("-------------------------------------------------------------------")
labels = np.array(labels)

# Adding a fourth dimension to the images array. This is "1" since we only have one color channel: grayscale.
images = images.reshape((images.shape[0], side_length, side_length, 1))

# Save the NumPy arrays for use in model.py, where the neural network is trained and validated on this data
np.save('images.npy', images)
np.save('labels.npy', labels)

print("\nNumPy files saved. Processing complete.")