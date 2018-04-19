import os
import cv2

from tqdm import tqdm
import random


class PicturePreparation:

    @staticmethod
    def prepare_images(path, stride):
        """
        Saves each frame of a movie as a list of consecutive frames
        """
        images = []
        if not os.path.exists('frames_from_movies'):
            os.mkdir('frames_from_movies')
        if not os.path.exists('test'):
            os.mkdir('test')

        picture_enumerator = 0
        for filename in os.listdir(path):
            video = cv2.VideoCapture(path + "/" + filename)

            success = True
            while success:
                success, image = video.read()
                images.append(image)

            video.release()

            if not os.path.exists('frames_from_movies/{}'.format(filename)):
                os.mkdir('frames_from_movies/{}'.format(filename))
            for index, image in tqdm(enumerate(images)):
                if image is not None:
                    resized = cv2.resize(image, (int(256), int(256)))
                    if index % stride == 0:
                        if (random.randrange(1,10,1) > 7):
                            gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                            cv2.imwrite("test/{}.png".format(picture_enumerator), gray_image)
                        else:
                            cv2.imwrite("frames_from_movies/{}/{}.png".format(filename,picture_enumerator), resized)
                    picture_enumerator += 1
            images.clear()