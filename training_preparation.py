import os
import random
import shutil


def get_images_from_directory(path, stride=1):
    """
    This function returns all png files from the given path argument.
    :param path: str with path to a folder
    :return: list
    """
    return [filename for filename in os.listdir(path)[::stride] if filename.endswith('.png')]


def get_random_images(iterable, p=0.3):
    """
    This function returns random n elements from an iterable.
    :param iterable: list of filenames
    :param p: float part of training set
    :return: list
    """
    return random.sample(iterable, k=int(len(iterable) * p))


def extract_frame_set(original_folder, destination_folder_name,stride=25):
    """
    This function copies images to a destination_folder_name.
    :param original_folder: str path to folder with original images
    :param destination_folder_name: folder in which chosen images will be saved
    :param n: int number of images (100 by default)
    """
    if os.path.isdir(destination_folder_name):
        shutil.rmtree(destination_folder_name)
    
    os.mkdir(destination_folder_name)

    movies = [directory for directory in os.listdir(original_folder) if os.path.isdir(os.path.join(original_folder, directory))]

    [os.mkdir(os.path.join(destination_folder_name, dirname)) for dirname in movies if not os.path.exists(os.path.join(destination_folder_name, dirname))]

    dir_images = [get_images_from_directory(os.path.join(original_folder, movie), stride) for movie in movies]

    for index, movie in enumerate(movies):
        [shutil.copy(original_folder + "/" + movie + '/' + x, destination_folder_name + "/" + movie + '/' + x) for x in dir_images[index]]

'''
def extract_testing_set(original_folder, testing_folder_name="testing_set"):
    if not os.path.isdir(testing_folder_name):
        os.mkdir(testing_folder_name)

    movies = [directory for directory in os.listdir(original_folder) if os.path.isdir(os.path.join(original_folder, directory))]

    dir_images = [get_images_from_directory(os.path.join(original_folder, movie), stride=1) for movie in movies]

    [os.mkdir(os.path.join(testing_folder_name, dirname)) for dirname in movies if not os.path.isdir(os.path.join(testing_folder_name, dirname))]

    for index, movie in enumerate(movies):
        [shutil.move(original_folder + "/" + movie + '/' + x, testing_folder_name + "/" + movie + '/' + x) for x in get_random_images(dir_images[index])]
'''



if __name__ == "__main__":
    # extract_training_files('frames_from_movies/', n=250)
    extract_frame_set('training_frames','training_set',50)
    extract_frame_set('testing_frames','testing_set',100)
    

