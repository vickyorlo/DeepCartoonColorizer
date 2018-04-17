from keras.layers import Conv2D, UpSampling2D, Input, Reshape, concatenate, MaxPooling2D, Dropout, BatchNormalization, GaussianDropout, AlphaDropout
from keras.layers.advanced_activations import PReLU
from keras.models import Model, load_model
from keras.preprocessing.image import img_to_array, load_img
from keras.optimizers import Adamax
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
from skimage.io import imsave
import keras
import numpy as np
import os
import tensorflow as tf



model = load_model('model_300e_1000pic_m.h5')


color_me = []
for filename in [filename for filename in os.listdir('test/')[0:25] if filename.endswith(".png")]:
    color_me.append(img_to_array(load_img('test/' + filename)))
color_me = np.array(color_me, dtype=float)
color_me = rgb2lab((1.0 / 255) * color_me)[:, :, :, 0] / 128
color_me = color_me.reshape(color_me.shape + (1,))


output = model.predict(color_me)
output = output * 128


if not os.path.exists('result1'):
    os.mkdir('result1')

for i in range(len(output)):
    cur = np.zeros((256, 256, 3))
    cur[:, :, 0] = color_me[i][:, :, 0] * 128
    cur[:, :, 1:] = output[i][:, :, :]
    imsave("result1/img_" + str(i) + ".png", lab2rgb(cur))