import sys
from argparse import ArgumentParser
from datetime import datetime
from math import floor
from re import IGNORECASE, findall
from warnings import simplefilter

import pandas as pd

from filter import filter
from log import log
from naive_bayes import NaiveBayes
from perceptron import Perceptron

simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=pd.errors.ParserWarning)
simplefilter(
    action='ignore', category=pd.core.common.SettingWithCopyWarning)
pd.set_option('display.max_colwidth', -1)


if __name__ == "__main__":
    start = datetime.now()
    log(f'Starting {sys.argv[0].split("/")[-1]} program..')

    parser = ArgumentParser(
        description='Program to filter spam messages and emails.')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='Parameter to choose when to log things related with the resolution.')

    parser.add_argument('-trt', '--train_threshold', type=float, default=0.70,
                        help='Parameter to pass the percentage to be used in train phase.')

    parser.add_argument('-tet', '--test_threshold', type=float, default=0.15,
                        help='Parameter to pass the percentage to be used in test phase.')

    parser.add_argument('-vat', '--validation_threshold', type=float,
                        default=0.15, help='Parameter to pass the percentage to be used in validation phase.')

    args = parser.parse_args()

    log(args)

    assert args.train_threshold + args.test_threshold + \
        args.validation_threshold == 1, 'The sum of all thresholds must be 1.'

    # Importing the data
    df = pd.read_csv('spam.csv', encoding='ANSI', usecols=['v1', 'v2'])
    df.columns = ['label', 'message']

    # Pre processing the imported data
    df['label'] = df['label'].apply(
        lambda label: -1 if label.lower() == 'ham' else 1)

    df['message'] = df['message'].apply(lambda document: document.lower())

    df['message'] = df['message'].apply(
        lambda document: findall(r"[a-z0-9']+", document, IGNORECASE))

    # Defining the threshholds to be used on training, tests and validation

    # in case we want to shuffle the dataframe before training
    # df = df.sample(frac=1).reset_index(drop=True)

    df_train = df[: floor(len(df)*args.train_threshold)]

    df_test = df[
        df_train.index[-1] + 1: floor(len(df)*(args.train_threshold + args.test_threshold))]
    df_test['classified_as'] = None

    df_validation = df[df_test.index[-1]+1:]
    df_validation['classified_as'] = None

    # Select test data
    train_documents, train_labels = list(
        df_train['message']), list(df_train['label'])

    # Filtering with Naive Bayes method
    print()
    nb = NaiveBayes(
        documents=train_documents,
        labels=train_labels,
        debug=args.debug
    )
    filter(nb, df_test.copy(), df_validation.copy())

    # Filtering with Perceptron
    print()
    perceptron = Perceptron(
        documents=train_documents,
        labels=train_labels,
        debug=args.debug
    )
    filter(perceptron, df_test.copy(), df_validation.copy())
