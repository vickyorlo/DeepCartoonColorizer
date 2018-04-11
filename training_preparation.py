import os
import random
import shutil


def get_images_from_directory(path):
    return [filename for filename in os.listdir(path) if filename.endswith('.png')]


def get_random_images(iterable, n_images=100):
    return random.choices(iterable, k=n_images)


def extract_training_files(original_folder, destination_folder_name='test_img_for_training', n_elements=100):
    if not os.path.isdir(destination_folder_name):
        os.mkdir(destination_folder_name)

    directory_contents = get_images_from_directory(original_folder)
    random_images_names = get_random_images(directory_contents, n_elements)

    [shutil.copy(original_folder + "/" + x, destination_folder_name + "/" + x) for x in random_images_names]


if __name__ == "__main__":
    extract_training_files('frames_from_movies/')
