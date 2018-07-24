import os
import argparse

from shutil import rmtree
from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from training_preparation import extract_frame_set, extract_testing_frames


def generate_all_frames(input_movies_folder):
    if os.path.exists('training_frames'):
        rmtree('training_frames')

    PicturePreparation().process_all_movies(input_movies_folder)


def extract_sets(stride):
    if not os.path.isdir('training_frames'):
        print('First generate training frames with -i option.')
        return

    extract_frame_set('training_frames', 'training_set', stride=stride)
    extract_testing_frames('training_frames', 'training_set', 'testing_set')


def main():
    parser = argparse.ArgumentParser(description='parser')
    parser.add_argument('-i', help='folder with movie to teach on')
    parser.add_argument('-o', help='folder with movies to color', default='testing_set')
    parser.add_argument('-m', help='the model file')
    parser.add_argument('-c', help='color only', action='store_true')
    parser.add_argument('-t', help='train model', action='store_true')
    parser.add_argument('-a', help='all automatic mode', action='store_true')
    parser.add_argument('-et', help='extract training set', action='store_true')
    parser.add_argument('-e', type=int, help='amount of epochs', default=1000)
    parser.add_argument('-b', type=int, help='batch_size', default=5)
    parser.add_argument('-s', type=int, help='how many files to skip when creating training set', default=50)
    args = parser.parse_args()

    input_movies_folder = args.i
    color_movies = args.o
    model = args.m
    epochs = args.e
    batch_size = args.b
    stride = args.s
    extract_training_frames = args.et

    if args.a:
        generate_all_frames(input_movies_folder)
        extract_sets(stride)
        nn = NeuralNetwork('training_set', epochs, batch_size)
        nn.run()
        colorizer = PictureColorization(nn.model, color_movies)
        colorizer.save()
        return

    # to generate all possible frames
    if args.i:
        generate_all_frames(input_movies_folder)
        return

    # to extract training set
    if extract_training_frames:
        extract_sets(stride)
        return

    # train model
    if os.path.isdir('training_set') and args.t:
        nn = NeuralNetwork('training_set', epochs, batch_size)
        nn.run()
        return

    # to color directory with a model
    if args.c and args.m:
        nn = NeuralNetwork('training_set', epochs, batch_size, model)
        colorizer = PictureColorization(nn.model, color_movies)
        colorizer.save()
        return


if __name__ == "__main__":
    main()
