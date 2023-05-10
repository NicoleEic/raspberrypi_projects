from PIL import Image
import numpy as np

DD='/home/pi/myCode/mypaint'
im = Image.open('sunflower.jpeg')
width, height = im.size
a = np.array(Image.Image.getdata(im))
a = a.reshape(width, height, a.shape[1])