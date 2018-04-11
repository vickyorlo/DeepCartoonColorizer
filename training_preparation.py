import os
import random
import shutil


def get_images_from_directory(path):
    """
    This function returns all png files from the given path argument.
    :param path: str with path to a folder
    :return: list
    """
    return [filename for filename in os.listdir(path) if filename.endswith('.png')]


def get_random_images(iterable, n=100):
    """
    This function returns random n elements from an iterable.
    :param iterable: list of filenames
    :param n: int number of random elements
    :return: list
    """
    return random.choices(iterable, k=n)


def extract_training_files(original_folder, destination_folder_name='test_img_for_training', n=100):
    """
    This function copies images to a destination_folder_name.
    :param original_folder: str path to folder with original images
    :param destination_folder_name: folder in which chosen images will be saved
    :param n: int number of images (100 by default)
    """
    if not os.path.isdir(destination_folder_name):
        os.mkdir(destination_folder_name)

    directory_contents = get_images_from_directory(original_folder)
    random_images_names = get_random_images(directory_contents, n)

    [shutil.copy(original_folder + "/" + x, destination_folder_name + "/" + x) for x in random_images_names]


if __name__ == "__main__":
    extract_training_files('frames_from_movies/', n=250)
