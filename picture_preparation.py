import os
import cv2


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

        return self.images

    def save_images(self):
        """
        Saves coloured and black&white images into two separate folders.
        """
        self.prepare_images()
        PicturePreparation.prepare_folders()
        for index, image in enumerate(self.images):
            cv2.imwrite("frames_from_movies/{}.png".format(index), image)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("bw_frames/{}.png".format(index), gray_image)

    @staticmethod
    def prepare_folders():
        """
        This function prepares folders for images.
        """
        if not os.path.exists('frames_from_movies'):
            os.mkdir('frames_from_movies')
        if not os.path.exists('bw_frames'):
            os.mkdir('bw_frames')
