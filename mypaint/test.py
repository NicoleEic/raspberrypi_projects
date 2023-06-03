import sys
from colorthief import ColorThief
from skimage import io
import numpy as np
import math
import colorsys
from matplotlib import pyplot as plt

fname = 'sunflower.jpeg'
color_thief = ColorThief(fname)
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=20)

img = io.imread(fname)
col_list = np.unique(img.reshape(-1, 3), axis=0)


def step(r, g, b, repetitions=10):
    lum = math.sqrt(.241 * r + .691 * g + .068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * repetitions)
    v2 = int(v * repetitions)
    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum
    return (h2, lum, v2)


def get_selection(picked, image_fpath, myrange = 100):
    img = io.imread(image_fpath)
    col_list = np.unique(img.reshape(-1, 3), axis=0)
    col_list = np.array(sorted(col_list, key=lambda color: step(color[0], color[1], color[2], 10)))
    i = np.where((col_list == picked).all(axis=1))[0][0]
    selection = col_list[i-myrange:i+myrange, :]
    return selection

col_list2 = np.array(sorted(col_list, key=lambda color: step(color[0], color[1], color[2], 10)))
plt.imshow([col_list2], aspect='auto', interpolation=None)

shifted = np.vstack((col_list2[1:, :], col_list2[0, :]))
d = np.linalg.norm(col_list2 - shifted, axis=1)




myrange = 100
picked = col_list2[1000]
i = np.where((col_list2 == picked).all(axis=1))[0][0]
selection = col_list2[i-myrange:i+myrange, :]



from sklearn.decomposition import FastICA
transformer = FastICA(n_components=2,
        random_state=0,
        whiten='unit-variance')
X_transformed = transformer.fit_transform(col_list2)
X_transformed.shape
