import os
import cv2

import tqdm


class PicturePreparation:
    def __init__(self, path):
        self.path = path
        self.images = []

    def prepare_images(self):
        """
        Saves each frame of a movie as a list of consecutive frames
        """
        video = cv2.VideoCapture(self.path)

        success = True
        while success:
            success, image = video.read()
            self.images.append(image)

        video.release()

    def save_images(self):
        """
        Saves coloured and black&white images into two separate folders.
        """
        self.prepare_images()
        PicturePreparation.prepare_folders()
        for index, image in tqdm(enumerate(self.images)):
            if not (image is None):
                resized = cv2.resize(image, (int(256), int(256)))
                if index < 79 or (index > 700 and index < 10500):
                    if index % 10:
                        cv2.imwrite("frames_from_movies/{}.png".format(index), resized)
                    else:
                        gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite("test/{}.png".format(index), gray_image)

    @staticmethod
    def prepare_folders():
        """
        This function prepares folders for images.
        """
        if not os.path.exists('frames_from_movies'):
            os.mkdir('frames_from_movies')
        if not os.path.exists('test'):
            os.mkdir('test')
