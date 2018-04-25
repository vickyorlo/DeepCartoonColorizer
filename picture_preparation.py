import os
import cv2
import random

from multiprocessing import Pool, cpu_count
from shutil import rmtree
from unidecode import unidecode


class PicturePreparation(object):

    def __init__(self, workers):
        self.workers = workers if workers else cpu_count()

    @staticmethod
    def prepare_images(path_to_directory, filename):
        """
        Saves each frame of a movie as a list of consecutive frames
        """
        if not os.path.exists('frames_from_movies'):
            os.mkdir('frames_from_movies')
            os.mkdir('test')

        if not os.path.exists('frames_from_movies/{}'.format(filename)):
            os.mkdir('frames_from_movies/{}'.format(filename))
            os.mkdir('test/{}'.format(filename))

        video = cv2.VideoCapture(os.path.join(path_to_directory, filename))
        success = True
        index = 0
        while success:
            success, image = video.read()

            if success:
                resized = cv2.resize(image, (int(256), int(256)))
                cv2.imwrite("frames_from_movies/{}/{}.png".format(filename, index), resized)
                gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("test/{}/{}.png".format(filename, index), gray_image)
            index += 1

        video.release()

    def process_all_movies(self, path):
        # if os.path.exists('frames_from_movies'):
        #     rmtree('frames_from_movies')
        #     rmtree('test')

        if not os.path.exists('frames_from_movies'):
            os.mkdir('frames_from_movies')

        if not os.path.exists('test'):
            os.mkdir('test')

        files_in_directory = os.listdir(path)

        os.chdir(path)
        [os.rename(filename, unidecode(filename)) for filename in files_in_directory]
        os.chdir("..")
        os.listdir(path)

        function_input = [(path, filename) for filename in files_in_directory]

        function_input = [argument for argument in function_input if not
                          os.path.exists(os.path.join('frames_from_movies', argument[1]))]

        with Pool(processes=self.workers) as pool:
            pool.starmap_async(PicturePreparation.prepare_images, function_input)
            pool.close()
            pool.join()


if __name__ == "__main__":
    pp = PicturePreparation(workers=1)
    pp.process_all_movies('filmy')
