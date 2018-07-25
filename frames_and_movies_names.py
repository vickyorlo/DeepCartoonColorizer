"""
This modile calculates number of frames in each cartoon folder.
"""

import os
import sys

try:
    movies = os.listdir(sys.argv[1])
except IndexError:
    print("Please specify folder as an imput.")
    sys.exit(0)

s = 0
for movie in movies:
    elements_in_path = len(os.listdir(os.path.join(sys.argv[1], movie)))
    print(movie, elements_in_path)
    s += elements_in_path

print('Summed {}'.format(s))
