from imagehash import phash
from scipy.spatial.distance import hamming
from PIL import Image

from merge_images.merge_images import zip_images


def evaluate_colorization(img1, img2):
    img1_hash = phash(img1)
    img2_hash = phash(img2)

    return hamming(img1_hash, img2_hash)


if __name__ == '__main__':
    zipped = zip_images('merge_images\\bajka1')

    for x, y in zipped:
        print(evaluate_colorization(Image.open(x), Image.open(y)))