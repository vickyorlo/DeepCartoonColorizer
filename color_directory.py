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

    def prepare_images(self):
        color_me = []
        for filename in [filename for filename in os.listdir(self.directory) if filename.endswith(".png")]:
            color_me.append(img_to_array(load_img(self.directory + '/' + filename)))
        color_me = np.array(color_me, dtype=float)
        color_me = rgb2lab((1.0 / 255) * color_me)[:, :, :, 0] / 128
        color_me = color_me.reshape(color_me.shape + (1,))

        return color_me

    def predict(self):
        images_for_colorization = self.prepare_images()
        output = self.model.predict(images_for_colorization)
        return output * 128

    def save(self, directory='test_result'):
        if not os.path.exists(directory):
            os.mkdir(directory)

        images_for_colorization = self.prepare_images()
        colorized_images = self.predict()

        for i in tqdm(range(len(colorized_images))):
            cur = np.zeros((256, 256, 3))
            cur[:, :, 0] = images_for_colorization[i][:, :, 0] * 128
            cur[:, :, 1:] = colorized_images[i][:, :, :]
            imsave(directory + "/img_" + str(i) + ".png", lab2rgb(cur))

