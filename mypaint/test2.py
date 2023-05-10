# Importing required boundaries
from skimage.segmentation import slic, mark_boundaries
from skimage.data import astronaut
from skimage import io
from matplotlib import pyplot as plt


# Setting the plot figure as 15, 15
plt.figure(figsize=(15, 15))

# Sample Image of scikit-image package

# astronaut = astronaut()
astronaut = io.imread('sunflower.jpeg')

# Applying SLIC segmentation
# for the edges to be drawn over
astronaut_segments = slic(astronaut,
						n_segments=20,
						compactness=1)

plt.subplot(1, 2, 1)

# Plotting the original image
plt.imshow(astronaut)

# Detecting boundaries for labels
plt.subplot(1, 2, 2)

# Plotting the output of marked_boundaries
# function i.e. the image with segmented boundaries
plt.imshow(mark_boundaries(astronaut, astronaut_segments))

plt.show()