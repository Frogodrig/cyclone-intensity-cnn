# Convolutional Neural Network (CNN) for Estimating Tropical Cyclone Wind Intensity Through Infrared Satellite Imagery
This repo contains the code to download and prepare data to train and validate a convolutional neural network. 
## Project Background and Motivation
Since cyclones are typically located over large bodies of water where weather stations are sparse, meteorologists often have to estimate the wind speed of cyclones. They usually use buoy observations, microwave satellite imagery, and infrared satellite imagery to make these estimates.

There is growing interest in applying AI and machine learning techniques to improve the accuracy of operational meteorological tasks, including estimating cyclone wind speed. I began looking into applying deep learning to cyclone wind speed estimation during the COVID-19 pandemic when the American Meteorological Society (AMS) made their journal articles publicly available at no cost. <a href="https://journals.ametsoc.org/mwr/article/147/6/2261/344590/Using-Deep-Learning-to-Estimate-Tropical-Cyclone">Wimmers et al. 2019</a> and <a href="https://journals.ametsoc.org/waf/article/34/2/447/291/Estimating-Tropical-Cyclone-Intensity-by-Satellite">Chen et al. 2019</a> both applied deep learning to cyclone wind speed estimation, achieving considerable accuracy. This piqued my interest, so I decided to take a stab at it.
## Data Sources
I used images of cyclones from the <a href="https://www.ncdc.noaa.gov/hursat/">HURSAT data project</a> run by the National Centers for Environmental Information. This database contains satellite images of cyclones in NetCDF file format. The best part about this database: the center of each cyclone was in the middle of each image.

I also used best track data from the <a href="https://www.nhc.noaa.gov/data/#hurdat">HURDAT2 database</a> provided by the National Hurricane Center. It contains records of all known cyclones in the Atlantic and Pacific basins, as well as their wind speeds at 6-hour intervals.
## Overview of Files

<b>`besttrack.csv`</b>: Contains the data cleaned from the National Hurricane Center's HURDAT2 database found at this <a href="https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2019-052520.txt">link</a>. `downloader.py` and `labelling.py` rely on this data to function properly.

<b>`downloader.py`</b>: Downloads the satellite images of cyclones from the HURSAT database as NetCDF files.

<b>`dataCleaner.py`</b>: Cleans the 'best track' data obtained in a .txt and converts it into a csv file

<b>`labelling.py`</b>: Labels satellite images of cyclones with their wind speed from the best track dataset. Saves these images and labels as NumPy array files.

<b>`viewImages.py`</b> (Optional): Does not play a pivotal role in running the model, but may be of interest to the curious developer. Shows 10 random images from the set of satellite images in `images.npy`.
## Highlights of Methodology
<b>Optimized Data Downloading</b>: `downloader.py` does not download files that cannot be used in the neural network. The HURSAT database has images of cyclones from around the world, but the best track data from HURDAT2 only contains wind speeds for cyclones from the Atlantic and Pacific Oceans. So, before downloading a cyclone’s satellite imagery from HURSAT, the code checks to see whether the best track data has records for that cyclone. If best track has no data for that cyclone, the satellite image is not downloaded. This conserves local storage space and cuts down on execution time.

<b>“Cropping” Satellite Images</b>: The most valuable information about a cyclone’s intensity is near the center. So, `labelling.py` crops satellite images to remove the outer part of the cyclone from the image. After reading the satellite image from its NetCDF file, turning it into a NumPy array, the code crops the image so that only a 50-by-50-pixel square at the center is remaining. 

<b>Merging HURSAT and HURDAT2 to Match Satellite Images with their Wind Speed</b>: Each satellite image file provides us with the name of the cyclone, as well as the time and date of the satellite image. However, it does not provide us with the wind speed of the cyclone at that time. `assemble.py` finds the wind speed for each satellite image by searching for the cyclone’s name, date, and time in the best track dataset. Once the wind speed is retrieved, both the satellite image and wind speed are appended to NumPy arrays in unison. This effectively labels the satellite image with its wind speed, since can the satellite image and wind speed will be retrieved in unison in `model.py`.


## Things that work as of now
1.	Create a directory to store the contents of this project
2.	Download `downloader.py`, `labelling.py`, 'dataCleaner.py' and `besttrack.csv` to this directory. 
3.	Run `downloader.py`, which will create a directory called `Satellite Imagery` where the satellite image files will be downloaded. <i>Warning</i>: one year of cyclone satellite images is about 500 MB. Multiple cyclone seasons can take up a GB or more of local storage.
4.	Run `dataCleaner.py`, which will create clean the 'best track' data and converts it into a csv format.
5.	Run `labelling.py`, which will create `images.npy` and `labels.npy` containing data prepared for training and validating the neural network.



