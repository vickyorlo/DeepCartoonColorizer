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

    def save(self, patch_size=256, results_folder="test_result"):
        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        for foldername in [x for x in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, x))]:
            if not os.path.isdir(os.path.join(results_folder, foldername)):
                os.mkdir(os.path.join(results_folder, foldername))
            
            for filename in tqdm([filename for filename in os.listdir(os.path.join(self.directory, foldername)) if filename.endswith(".png")]):
                color_me = img_to_array(load_img(f"{self.directory}/{foldername}/{filename}"))
                color_me = rgb2lab((1.0 / 255) * color_me)[:, :, 0] / 512
                color_me = color_me.reshape(color_me.shape +(1,))
                result = np.zeros((256,256,3))
                for y in range(0,256,patch_size):
                    for x in range(0,256,patch_size):
                        patch = color_me[x:x+patch_size,y:y+patch_size]
                        output = self.model.predict(np.array([patch]))
                        output *= 512
                        cur = np.zeros((patch_size, patch_size, 3))
                        cur[:, :, 0] = patch[:, :, 0] * 512
                        cur[:, :, 1:] = output[0][:, :, :]
                        result[x:x+patch_size,y:y+patch_size] = cur
                imsave(f"{results_folder}/{foldername}/{filename}", lab2rgb(result))
