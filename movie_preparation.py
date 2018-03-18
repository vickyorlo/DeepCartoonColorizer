import os
import cv2


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
        for image_number in range(n_images):
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

        for image in images:
            movie.write(image)
        movie.release()
