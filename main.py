import os
import sys
import argparse

from shutil import rmtree
from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation
from training_preparation import extract_testing_set, extract_training_set


def main():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-i', help='folder with movie files')
    parser.add_argument('-m', help='the model file')
    parser.add_argument('-c', help='color only')
    parser.add_argument('-e', type=int, help='amount of epochs', default=10)
    parser.add_argument('-b', type=int, help='batch_size', default=1)
    parser.add_argument('-s', type=int, help='how many files to skip when creating learning set', default=25)
    args = parser.parse_args()

    input_movies = args.i
    model = args.m
    epochs = args.e
    batch_size = args.b
    stride = args.s

    if args.i:
        rmtree('frames_from_movies')
        PicturePreparation().process_all_movies(input_movies)

    if args.c and args.m:
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size, model)
        colorizer = PictureColorization(nn.model, "testing_set/")
        colorizer.save()
    elif args.m and os.path.isfile(model):
        extract_training_set('frames_from_movies', stride=stride)
        extract_testing_set('frames_from_movies')

        nn = NeuralNetwork('frames_from_movies', epochs, batch_size, model)
        nn.run()

        colorizer = PictureColorization(nn.model, "testing_set/")
        colorizer.save()
    elif os.path.isdir('frames_from_movies'):
        extract_training_set('frames_from_movies', stride=stride)
        extract_testing_set('frames_from_movies')
        
        nn = NeuralNetwork('frames_from_movies', epochs, batch_size)
        nn.run()

        colorizer = PictureColorization(nn.model, "testing_set/")
        colorizer.save()

    # movie_prep = MoviePreparation('bw_frames')
    # movie_prep.save_movie()


if __name__ == "__main__":
    main()