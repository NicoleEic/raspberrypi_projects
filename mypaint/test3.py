# Importing required libraries
from skimage.segmentation import slic
from skimage.data import astronaut
from skimage.color import label2rgb
from skimage import io
from matplotlib import pyplot as plt
from skimage.segmentation import felzenszwalb, slic, quickshift, watershed
import numpy as np


# Setting the plot size as 15, 15
plt.figure(figsize=(15,15))

# Sample Image of scikit-image package
# astronaut = astronaut()
astronaut = io.imread('sunflower.jpeg')

# Applying Simple Linear Iterative
# Clustering on the image
# - 50 segments & compactness = 10
# astronaut_segments = slic(astronaut,
# 						n_segments=10,
# 						compactness=1)
astronaut_segments = felzenszwalb(astronaut,
                                  scale=1000,
                                  sigma=1,
                                  min_size=500)

plt.imshow(astronaut_segments)
plt.show()
