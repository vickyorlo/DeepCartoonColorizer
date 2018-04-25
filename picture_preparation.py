# -*- coding: utf-8 -*-

import os
import cv2
import random

from tqdm import tqdm
from multiprocessing import Pool
from shutil import rmtree
from unidecode import unidecode


class PicturePreparation(object):

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

    @staticmethod
    def process_all_movies(path):
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

        function_input = [argument for argument in function_input if os.path.exists(os.path.join(argument[0], argument[1]))]

        print(function_input)
        with Pool(processes=2) as pool:
            pool.starmap_async(PicturePreparation.prepare_images, function_input)
            pool.close()
            pool.join()


if __name__ == "__main__":
    pp = PicturePreparation()
    # pp.prepare_images('filmy', u"Teraz Miki! - Jak grać w baseball.mp4")

    pp.process_all_movies('filmy')
