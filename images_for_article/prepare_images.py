import cv2
import os
import numpy as np


def process_image(images):
    resulting_image = np.empty(shape=(0, 256*3, 3))
    for index, img in enumerate(images):
        image = cv2.imread(img)

        original, colored = image[:, :256], image[:, 256:]
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        gray_3d = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        row = np.concatenate((gray_3d, original, colored), axis=1)

        resulting_image = np.append(resulting_image, row, axis=0)

    return resulting_image


if __name__ == '__main__':

    try:
        os.chdir(os.path.join(os.getcwd(), 'image', 'seen'))
        os.remove("result.png")
    except FileNotFoundError:
        pass

    images = [x for x in os.listdir(os.path.join(os.getcwd())) if x.endswith('png')]
    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    img = process_image(images)
    cv2.imwrite("result.png", img)
