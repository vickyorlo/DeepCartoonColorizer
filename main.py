import os
import sys
import argparse

from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation

if __name__ == "__main__":
    main()


def main(self):
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-i', help='folder with movie files')
    parser.add_argument('-m', help='the model file')
    parser.add_argument('-e', type=int, help='amount of epochs')
    args = parser.parse_args()

    movies = args.i
    model = args.m
    epochs = args.e

    if model is not None and os.path.isfile(model):
        nn = NeuralNetwork('frames_from_movies', epochs, model)
        if input is not None and os.path.isdir(movies):
            pic_prepare = PicturePreparation(movies)
            pic_prepare.save_images()
            nn.run()

        colorizer = PictureColorization(nn.model, "test")
        colorizer.save()
    elif input is not None and os.path.isdir(movies):
        pic_prepare = PicturePreparation(movies)
        pic_prepare.save_images()
        nn = NeuralNetwork('frames_from_movies', epochs)
        nn.run()

    # movie_prep = MoviePreparation('bw_frames')
    # movie_prep.save_movie()
