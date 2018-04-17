import os
import sys

from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation


def main(argv):
    opts = dict()
    while argv:
        if argv[0][0] == '-':
            opts[argv[0]] = argv[1]
        argv = argv[1:]

    if '-i' in opts:
        input = opts['-i']
    else:
        input = None
    if '-m' in opts:
        model = opts['-m']
    else:
        model = None
    if '-e' in opts:
        epochs = opts['-e']
    else:
        epochs = None

    if model is not None and os.path.isfile(model):
        nn = NeuralNetwork('frames_from_movies', model, epochs)
        if input is not None and os.path.isdir(input):
            pic_prepare = PicturePreparation(input)
            pic_prepare.save_images()
            nn.run()

        colorizer = PictureColorization(nn.model, "test")
        colorizer.save()
    elif input is not None and os.path.isdir(input):
        pic_prepare = PicturePreparation(input)
        pic_prepare.save_images()
        nn = NeuralNetwork('frames_from_movies', epochs)
        nn.run()

    # movie_prep = MoviePreparation('bw_frames')
    # movie_prep.save_movie()
