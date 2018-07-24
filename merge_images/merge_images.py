import cv2
import os
import numpy as np
from tqdm import tqdm


BF_FOLDER_NAME = 'bw'
COLORED_FOLDER_NAME = 'colored'


def get_movies(directory):
    return [x for x in os.listdir(directory) if os.path.isdir(x) and not x.startswith("__")]


def build_path_to_images(movie_directory, type):
    return os.path.join(os.getcwd(), movie_directory, type)


def zip_images(movie_directory):
    bw_path = build_path_to_images(movie_directory, 'bw')
    colored_path = build_path_to_images(movie_directory, 'colored')

    bw_images = [filename for filename in os.listdir(bw_path) if filename.endswith('.png')]
    colored_images = [filename for filename in os.listdir(colored_path) if filename.endswith('.png')]

    bw_images = sorted(bw_images, key=lambda x: int(x.split('.')[0]))
    colored_images = sorted(colored_images, key=lambda x: int(x.split('.')[0]))

    bw_images = [os.path.join(bw_path, x) for x in bw_images]
    colored_images = [os.path.join(colored_path, x) for x in colored_images]

    return zip(bw_images, colored_images)


def merge_two_images(img1, img2):
    return np.concatenate((img1, img2), axis=1)


def run(directory):
    movies = get_movies(directory)

    for movie in movies:
        paths = zip_images(movie)

        save_folder_path = os.path.join(os.getcwd(), directory, movie, 'merged_' + movie)

        if not os.path.isdir(save_folder_path):
            os.mkdir(save_folder_path)
        else:
            continue

        for index, paths in tqdm(enumerate(paths)):
            bw_img = cv2.imread(paths[0])
            col_img = cv2.imread(paths[1])

            merged_images = merge_two_images(bw_img, col_img)

            cv2.imwrite(save_folder_path + '/{}.png'.format(index), merged_images)


if __name__ == '__main__':
    run(os.getcwd())
