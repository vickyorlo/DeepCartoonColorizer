from imagehash import phash
from scipy.spatial.distance import hamming
from PIL import Image

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


if __name__ == '__main__':
    zipped = zip_images('merge_images\\bajka1')
    #
    for x, y in zipped:
        print(evaluate_colorization(Image.open(x), Image.open(y)))

    # print(hamming2('Dawid', 'Dawid'))