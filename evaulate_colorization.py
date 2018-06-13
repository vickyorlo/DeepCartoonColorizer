from imagehash import phash
from scipy.spatial.distance import hamming
from PIL import Image


def evaluate_colorization(img1, img2):
    img1_hash = phash(img1)
    img2_hash = phash(img2)

    print(img1_hash, img2_hash)

    return hamming(img1_hash, img2_hash)


if __name__ == '__main__':
    img1 = Image.open(r'C:\Users\Dawid\Desktop\ComputerScientistColoringBook\merge_images\bajka1\colored\500.png')
    img2 = Image.open(r'C:\Users\Dawid\Desktop\ComputerScientistColoringBook\merge_images\bajka1\bw\600.png')

    value = evaluate_colorization(img1, img2)

    print(value)