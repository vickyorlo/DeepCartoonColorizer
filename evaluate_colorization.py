import cv2
import os
import logging

import matplotlib.pyplot as plt
import numpy as np

from skimage.measure import compare_ssim as ssim
from merge_images.merge_images import zip_images

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


def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    return sum(c1 != c2 for c1, c2 in zip(list(s1), list(s2)))


def calculate_ssim(img1_path, img2_path):
    return ssim(cv2.imread(img1_path), cv2.imread(img2_path), multichannel=True)


def get_histogram(img1_path, img2_path):
    img1 = cv2.imread(img1_path).astype(np.int8)
    img2 = cv2.imread(img2_path).astype(np.int8)

    def get_channels(img1, img2):
        for ch in range(img1.shape[-1]):
            yield np.subtract(img1[:, :, ch], np.array(img2[:, :, ch]))

    channels_generator = get_channels(img1, img2)

    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(8, 2))
    for index, channel in enumerate(channels_generator):
        ax[index].hist(channel.ravel(), bins=range(channel.min(), channel.max()))

    plt.tight_layout()
    plt.savefig('h' + img1_path.split('\\')[-1])
    # plt.show()


if __name__ == '__main__':
    cartoons = [x for x in os.listdir('merge_images') if
                os.path.isdir(os.path.join('merge_images', x)) and not x.startswith('__')]

    for c in cartoons:
        zipped = zip_images(os.path.join('merge_images', c))
        # try:
        #     training_set = os.listdir(os.path.join('training_set', c))
        # except Exception as e:
        #     logger.error(e)
        #     continue

        # result = []
        for x, y in zipped:

            # if x.split('/')[-1] in training_set:
            #     continue

            get_histogram(x, y)

        #     ssim_image_comparison_value = ssim(cv2.imread(x), cv2.imread(y), multichannel=True)
        #     result.append(ssim_image_comparison_value)
        #     logger.info(f'{c} {x.split("/")[-1]} {str(ssim_image_comparison_value)}')
        #
        # result = np.array(result)
        # print(c, np.average(result), np.std(result), np.median(result))
        # logger.info(f'{c}, {str(np.average(result))}, {str(np.std(result))}, {str(np.median(result))}')
        # result = []
