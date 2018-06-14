import os
import sys
import argparse

from shutil import rmtree
from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation
from training_preparation import extract_frame_set


def main():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-i', help='folder with movie to teach on')
    parser.add_argument('-o', help='folder with movies to color')
    parser.add_argument('-m', help='the model file')
    parser.add_argument('-c', help='color only')
    parser.add_argument('-e', type=int, help='amount of epochs', default=10)
    parser.add_argument('-b', type=int, help='batch_size', default=1)
    parser .add_argument('-s', type=int, help='how many files to skip when creating learning set', default=25)
    args = parser.parse_args()

    input_movies = args.i
    color_movies = args.o
    model = args.m
    epochs = args.e
    batch_size = args.b
    stride = args.s

    if args.i:
        if os.path.exists('frames_from_movies'):
            rmtree('frames_from_movies')
            
        PicturePreparation().process_all_movies(input_movies,color_movies)

    if args.c and args.m:
        nn = NeuralNetwork('training_set', epochs, batch_size, model)
        colorizer = PictureColorization(nn.model, "movies_set")
        colorizer.save()
    elif args.m and os.path.isfile(model):
        extract_frame_set('training_frames','training_set',stride=stride)
        extract_frame_set('testing_frames','testing_set',stride=2*stride)
        nn = NeuralNetwork('training_set', epochs, batch_size, model)
        nn.run()

        colorizer = PictureColorization(nn.model, "testing_set/")
        colorizer.save()
    elif os.path.isdir('frames_from_movies'):
        extract_frame_set('training_frames','training_set',stride=stride)
        extract_frame_set('testing_frames','testing_set',stride=2*stride)        
        nn = NeuralNetwork('training_set', epochs, batch_size)
        nn.run()

        colorizer = PictureColorization(nn.model, "testing_set/")
        colorizer.save()

    # movie_prep = MoviePreparation('bw_frames')
    # movie_prep.save_movie()


if __name__ == "__main__":
    main()