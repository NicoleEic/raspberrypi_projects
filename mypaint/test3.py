# Importing required libraries
from skimage.segmentation import slic
from skimage.data import astronaut
from skimage.color import label2rgb
from skimage import io
from matplotlib import pyplot as plt
from skimage.segmentation import felzenszwalb, slic,  mark_boundaries, find_boundaries
import numpy as np
import skimage.color as color

fname = 'fruit.jpg'
img = io.imread(fname)

# Clustering on the image
img_segments = felzenszwalb(img,
                          scale=300,
                          sigma=2,
                          min_size=1000)


print(len(np.unique(img_segments)))
plt.subplot(1, 2, 1)

plt.imshow(color.label2rgb(img_segments, img, kind='avg'))

plt.subplot(1, 2, 2)
plt.imshow(find_boundaries(img_segments).astype(np.uint8))

plt.show()

cols = color.label2rgb(img_segments, img, kind='avg')
cols = cols.reshape(-1, cols.shape[-1])
cols = np.unique(cols, axis=0)


print('done')
