import pandas as pd
import os
import logging
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create handlers and set levels
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler("extract_best_worse_middle_colorization.log")
stream_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

# create formatters and add them to handlers
stream_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)

# add handlers to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


def main():
    data = pd.read_excel('best_middle_worst_colorization.xlsx', None)

    if not os.path.isdir('extract_best_worse_middle_colorization'):
        os.mkdir('extract_best_worse_middle_colorization')

    for sheet_name, content in data.items():
        for index, row in content.iterrows():
            cartoon = row['cartoon']
            image_number = row['image_number']
            value = row.iat[2]
            path = os.path.join('merge_images', cartoon, 'merged_{}'.format(cartoon), image_number)
            logger.info(path)
            new_name = '{}-{}-{}-{}'.format(sheet_name.split('.')[0], value, cartoon, image_number)
            logger.info(new_name)

            try:
                shutil.copy2(path, os.path.join('extract_best_worse_middle_colorization', new_name))
            except Exception as e:
                logger.exception(e)
                logger.error(path)
                logger.error(new_name)


if __name__ == '__main__':
    main()
