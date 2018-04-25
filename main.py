import os
import sys
import argparse

from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation


def main():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-i', help='folder with movie files')
    parser.add_argument('-m', help='the model file')
    parser.add_argument('-c', help='color only')
    parser.add_argument('-e', type=int, help='amount of epochs', default=10)
    parser.add_argument('-b', type=int, help='batch_size', default=1)
    parser.add_argument('-s', type=int, help='how many files to skip when creating learning set', default=25)
    args = parser.parse_args()

    movies = args.i
    model = args.m
    epochs = args.e
    batch_size = args.b
    stride = args.s

    if args.c and args.m:
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size, model)
        colorizer = PictureColorization(nn.model, "test/")
        colorizer.save()

    if model and os.path.isfile(model):
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size, model)
        if movies is not None and os.path.isdir(movies):
            PicturePreparation().prepare_images(movies,stride)
            nn.run()

        colorizer = PictureColorization(nn.model, "test/")
        colorizer.save()
    
    elif movies and os.path.isdir(movies):
        PicturePreparation().prepare_images(movies,stride)
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size)
        nn.run()
    elif os.path.isdir('frames_from_movies'):
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size)
        nn.run()

    # movie_prep = MoviePreparation('bw_frames')
    # movie_prep.save_movie()


if __name__ == "__main__":
    main()