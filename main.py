import os
import sys

from picture_preparation import PicturePreparation
from neural_network import NeuralNetwork
from color_directory import PictureColorization
from movie_preparation import MoviePreparation

try:
    filename = sys.argv[1]
except IndexError:
    print('Please input filename as first argument.')
    sys.exit(0)

if not os.path.isfile(filename):
    print("No file {} in the directory".format(filename))
    sys.exit(0)

pic_prepare = PicturePreparation(filename)
pic_prepare.save_images()

nn = NeuralNetwork('frames_from_movies', epochs=1)
nn.run()

colorizer = PictureColorization(nn.model, "test")
colorizer.save()

# movie_prep = MoviePreparation('bw_frames')
# movie_prep.save_movie()