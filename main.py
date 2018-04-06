import os
import sys

from picture_preparation import PicturePreparation
from movie_preparation import MoviePreparation

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("No file {} in the directory".format(filename))
    sys.exit(0)

pic_prepare = PicturePreparation(filename)
pic_prepare.save_images()


#movie_prep = MoviePreparation('bw_frames')
#movie_prep.save_movie()
