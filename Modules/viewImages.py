# view_images.py
#
# Purpose of this file:
# This file is not an exxential part of preparing data or running the neural network. It gives the user a view of
# what the images of cyclones look like. These are the images that the neural network is trained on in model.py
#
# Outline of this file:
# - Reads numpy files containing cyclone images and the wind speed they are associated with
# - Shows 10 random satellite images and their wind speeds
# - When running the script, closing the current matplotlib window will cause the next one to open


import numpy as np
import matplotlib.pyplot as plt
import random

images = np.load('images.npy')
# print(images.shape)
labels = np.load('labels.npy')
# print(labels.shape)

for x in range(10):
    i = random.randint(0, images.shape[0])
    image = np.reshape(images[i], (images[i].shape[0], images[i].shape[1]))
    # print(image.shape) (64, 64)
    plt.imshow(image, cmap='binary')
    plt.title('Image #' + str(i) + '   ' + str(labels[i]) + ' knots')
    plt.show()