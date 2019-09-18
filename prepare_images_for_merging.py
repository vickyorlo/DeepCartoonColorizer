"""
This module copy original images and colored images to folders from which consecutive frames will be merged side by side.
"""
import os
import shutil
from tqdm import tqdm

RESULT_FOLDER = 'test_result'

movies = os.listdir(RESULT_FOLDER)

def picture_prepare_for_merging():
    for movie in tqdm(movies):
        if not os.path.isdir(os.path.join('merge_images', movie)):
            os.mkdir(os.path.join('merge_images', movie))

            shutil.copytree(os.path.join('testing_set', movie), os.path.join('merge_images', movie, 'bw'))
            shutil.copytree(os.path.join(RESULT_FOLDER, movie), os.path.join('merge_images', movie, 'colored'))

if __name__ == '__main__':
    picture_prepare_for_merging()
