from imagehash import phash
from scipy.spatial.distance import hamming
from skimage.measure import compare_ssim as ssim
from PIL import Image
import numpy as np
import cv2
import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('evaluate_colorization.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

from merge_images.merge_images import zip_images


def evaluate_colorization(img1, img2):
    """Calculate hamming distance between two hashes"""
    img1_hash = phash(img1)
    img2_hash = phash(img2)

    print(img1_hash, img2_hash)

    return img1_hash - img2_hash


def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    return sum(c1 != c2 for c1, c2 in zip(list(s1), list(s2)))


def calculate_ssim(img1_path, img2_path):
    return ssim(cv2.imread(img1_path), cv2.imread(img2_path), multichannel=True)


if __name__ == '__main__':
    cartoons = [x for x in os.listdir('merge_images') if os.path.isdir(os.path.join('merge_images', x)) and not x.startswith('__')]

    for c in cartoons:
        zipped = zip_images(os.path.join('merge_images', c))
        try:
            training_set = os.listdir(os.path.join('training_set', c))
        except Exception as e:
            logger.error(e)
            continue
        
        result = []
        for x, y in (zipped):

            if x.split('/')[-1] in training_set:
                continue

            result.append(ssim(cv2.imread(x), cv2.imread(y), multichannel=True))

        result = np.array(result)
        print(c, np.average(result), np.std(result), np.median(result))
        logger.info(f'{c}, {str(np.average(result))}, {str(np.std(result))}, {str(np.median(result))}')
        result = []
