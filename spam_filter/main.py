import argparse
import re
import warnings
from datetime import datetime
from math import floor

import pandas as pd

from nb_filter import nb_filter

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.ParserWarning)
warnings.simplefilter(
    action='ignore', category=pd.core.common.SettingWithCopyWarning)


if __name__ == "__main__":
    start = datetime.now()
    print(f'Starting program at {start}')

    parser = argparse.ArgumentParser(
        description='Program to filter spam messages and emails.')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Parameter to choose when to log things related with the resolution.')
    args = parser.parse_args()

    # Importing the data
    pd.set_option('display.max_colwidth', -1)
    documents = pd.read_csv('documents.csv', sep=r'\t',
                            header=None)

    documents.columns = ['label', 'message']

    # Pre processing the imported data
    documents['message'] = documents['message'].apply(
        lambda document: document.lower())

    documents['message'] = documents['message'].apply(
        lambda document: re.findall(r"[a-z0-9']+", document, re.IGNORECASE))

    # Defining the threshholds to be used on training, tests and validation
    train_threshold = (0, floor(len(documents) * 0.7))
    test_threshold = (train_threshold[1] + 1, floor(len(documents) * 0.85))
    validation_threshold = (test_threshold[1] + 1, len(documents))

    # Filtering with Naive Bayes method
    nb_filter(documents, train_threshold, test_threshold, validation_threshold)

    # Filtering with Perceptron
