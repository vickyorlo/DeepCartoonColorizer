import cv2
import os
import numpy as np


def process_image(images):
    resulting_image = np.empty(shape=(0, 256*2, 3))
    for index, img in enumerate(images):
        image = cv2.imread(img)

        original, colored = image[:, :256], image[:, 256:]
        gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
        gray_3d = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        row = np.concatenate((original, colored), axis=1)

        resulting_image = np.append(resulting_image, row, axis=0)

    img = np.hstack((resulting_image[:1536], resulting_image[1536:]))

    return img


if __name__ == '__main__':

    try:
        os.chdir(os.path.join(os.getcwd(), 'image', 'unseen'))
        os.remove("result.png")
    except FileNotFoundError:
        pass

    images = [x for x in os.listdir(os.path.join(os.getcwd())) if x.endswith('png')]
    images = sorted(images, key=lambda x: int(x.split('.')[0]))

    # print(images)

    l = ['2626.png', '2982.png', '3615.png', '3223.png', '4151.png', '8505.png', '5380.png', '6322.png', '7250.png', '7621.png', '8706.png', '9775.png']

    img = process_image(l)
    cv2.imwrite("result1.png", img)
