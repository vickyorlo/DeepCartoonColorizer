import cv2
import os

MOVIES_FOLDER = 'filmy'

def main():
    movies = [x for x in os.listdir(os.path.join('..', MOVIES_FOLDER)) if not x.endswith('.py')]

    for movie in movies:
        movie_path = os.path.join('..', MOVIES_FOLDER, movie)

        video = cv2.VideoCapture(movie_path)

        success = True
        while success:
            success, image = video.read()

            if success:
                print('{:<60} {}'.format(movie, image.shape))
                break

        video.release()


if __name__ == '__main__':
    main()
