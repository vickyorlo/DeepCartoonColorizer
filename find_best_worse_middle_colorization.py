import logging
import os
import pandas as pd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create handlers and set levels
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler("extract_colorizations.log")
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


def get_best(df, column=None, n=1):
    return df.iloc[:n][['cartoon', 'image_number', column]]


def get_worst(df, column=None, n=1):
    return df.iloc[-n:][['cartoon', 'image_number', column]]


def get_middle(df, column=None, n=1):
    middle = df.shape[0] // 2
    return df.iloc[middle: middle + n][['cartoon', 'image_number', column]]


def get_colorization(df, column=None, n=1):
    if not column:
        logger.error("Wrong column name.")
        return None

    sorted_df = df.sort_values(column, ascending=False)

    best = get_best(sorted_df, column, n)
    worst = get_worst(sorted_df, column, n)
    middle = get_middle(sorted_df, column, n)

    return best, worst, middle


def process_all_cartoons(df, column=None, n=1):
    grouped = df.groupby('cartoon')

    extracted_best = pd.DataFrame()
    extracted_worst = pd.DataFrame()
    extracted_middle = pd.DataFrame()

    for name, data in grouped:
        best, worst, middle = get_colorization(data, column, n)
        extracted_best = extracted_best.append(best, ignore_index=True)
        extracted_worst = extracted_worst.append(worst, ignore_index=True)
        extracted_middle = extracted_middle.append(middle, ignore_index=True)

    return extracted_best, extracted_worst, extracted_middle


def main():
    df = pd.read_csv('all_frames.csv', index_col=0)

    tests = ['nhd', 'ssim', 'ms-ssim', 'uqi', 'haar_psi']

    writer = pd.ExcelWriter('best_middle_worst_colorization.xlsx', engine='xlsxwriter')
    for test in tests:
        best, worst, middle = process_all_cartoons(df, test, 2)
        # best.to_csv('best_{}.csv'.format(test))
        # worst.to_csv('worst_{}.csv'.format(test))
        # middle.to_csv('middle_{}.csv'.format(test))

        best.to_excel(writer, 'best_{}.csv'.format(test))
        worst.to_excel(writer, 'worst_{}.csv'.format(test))
        middle.to_excel(writer, 'middle_{}.csv'.format(test))


if __name__ == '__main__':
    main()
