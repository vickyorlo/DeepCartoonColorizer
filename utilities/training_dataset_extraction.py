import os
import json

TRAININD_DATASET_FOLDER_NAME = 'training_set'


def main():
    training_set_path = os.path.join('..', TRAININD_DATASET_FOLDER_NAME)

    folder_content = os.listdir(training_set_path)

    d = {}
    for cartoon in folder_content:
        d[cartoon] = os.listdir(os.path.join(training_set_path, cartoon))

    with open('training_dataset.json', 'w') as file:
        json.dump(d, file)


if __name__ == '__main__':
    main()