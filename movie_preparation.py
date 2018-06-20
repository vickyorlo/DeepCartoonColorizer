import os
import cv2
import sys

from tqdm import tqdm


class MoviePreparation:
    def __init__(self, directory):
        self.directory = directory

    def __prepare_images_for_movie(self):
        """
        This function prepares images for a movie.
        :return: list of images
        """
        images = []
        n_images = len([image for image in os.listdir(self.directory) if image.endswith('.png')])
        for image_number in tqdm(range(n_images)):
            image = "{}.png".format(image_number)
            images.append(cv2.imread(os.path.join(self.directory, image)))

        return images

    def save_movie(self, framerate=25, name='movie.avi'):
        """
        This function makes a movie from set of pictures.
        :param name: Holds information about the output movie filename ('movie.avi' by default).
        """
        images = self.__prepare_images_for_movie()
        height, width, _ = images[0].shape

        movie = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'DIVX'), framerate, (width, height))

        for image in tqdm(images):
            movie.write(image)
        movie.release()


if __name__ == "__main__":

    try:
        if sys.argv[1]:
            mp = MoviePreparation(sys.argv[1])
            mp.save_movie()
    except IndexError:
        MOVIES_TO_BE_MERGED = 'merge_images'
        print(f"Coloring all cartoons in {MOVIES_TO_BE_MERGED} folder.")

        movies = [x for x in os.listdir(MOVIES_TO_BE_MERGED) if not x.startswith('__') and not x.endswith('.py')]

        for movie in tqdm(movies):
            mp = MoviePreparation(os.path.join(MOVIES_TO_BE_MERGED, movie, 'merged_{}'.format(movie)))
            mp.save_movie(name=f'merged_{movie}')
