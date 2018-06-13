from keras.models import Model, load_model
from keras.preprocessing.image import img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb
from skimage.io import imsave
import numpy as np
import os
from tqdm import tqdm


class PictureColorization(object):
    def __init__(self, model, directory):
        self.model = model
        self.directory = directory

    def save(self, directory='test_result'):
        if not os.path.exists(directory):
            os.mkdir(directory)

        for filename in [filename for filename in os.listdir(self.directory) if filename.endswith(".png")]:
            color_me = img_to_array(load_img(self.directory + '/' + filename))
            color_me = rgb2lab((1.0 / 255) * color_me)[:, :, 0] / 512
            color_me = color_me.reshape(color_me.shape +(1,))
            print(color_me.shape)
            output = self.model.predict(np.array([color_me]))
            output *= 512
            print(output.shape)
            cur = np.zeros((256, 256, 3))
            cur[:, :, 0] = color_me[:, :, 0] * 512
            cur[:, :, 1:] = output[0][:, :, :]
            imsave(directory + "/" + filename, lab2rgb(cur))

