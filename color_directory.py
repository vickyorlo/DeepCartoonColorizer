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

    def save(self, results_folder="test_result"):
        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        for foldername in [x for x in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, x))]:
            if not os.path.isdir(os.path.join(results_folder, foldername)):
                os.mkdir(os.path.join(results_folder, foldername))
            
            for filename in [filename for filename in os.listdir(os.path.join(self.directory, foldername)) if filename.endswith(".png")]:
                color_me = img_to_array(load_img(f"{self.directory}/{foldername}/{filename}"))
                color_me = rgb2lab((1.0 / 255) * color_me)[:, :, 0] / 512
                color_me = color_me.reshape(color_me.shape +(1,))
                output = self.model.predict(np.array([color_me]))
                output *= 512
                cur = np.zeros((256, 256, 3))
                cur[:, :, 0] = color_me[:, :, 0] * 512
                cur[:, :, 1:] = output[0][:, :, :]
                imsave(f"{results_folder}/{foldername}/{filename}", lab2rgb(cur))

