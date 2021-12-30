import sys
from argparse import ArgumentParser
from ast import literal_eval
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

    parser.add_argument('-rcsv', '--read_csv', action='store_true',
                        help='Whether the program should read the original csv or use the treated one.')

    args = parser.parse_args()

    log(args)

    assert args.train_threshold + args.test_threshold + \
        args.validation_threshold == 1, 'The sum of all thresholds must be 1.'

    if args.read_csv:
        log('Importing the source csv and treating it.')
        df = pd.read_csv('spam.csv', encoding='ANSI', usecols=['v1', 'v2'])
        df.columns = ['label', 'message']

        # Pre processing the imported data
        df['label'] = df['label'].apply(
            lambda label: -1 if label.lower() == 'ham' else 1)

        df['message'] = df['message'].apply(lambda document: document.lower())

        df['message'] = df['message'].apply(
            lambda document: findall(r"[a-z0-9']+", document, IGNORECASE))

        # to shuffle the dataframe before training
        # df = df.sample(frac=1).reset_index(drop=True)
        # df.to_parquet('df_treated.parquet', index=False)
        # exit()

    else:
        log('Using treated dataframe as default.')
        df = pd.read_parquet('df_treated.parquet')
        # print(df)

        # for i, row in df.iterrows():
        #     print(type(row['label']), type(row['message']))
        #     print(row)
        #     print(row['message'][0])
        #     exit()

    # Defining the threshholds to be used on training, tests and validation
    df_train = df[: floor(len(df)*args.train_threshold)]

    df_validation = df[
        df_train.index[-1] + 1: floor(len(df)*(args.train_threshold + args.validation_threshold))]
    df_validation['classified_as'] = None

    df_test = df[df_validation.index[-1]+1:]
    df_test['classified_as'] = None

    # Select test data
    train_documents, train_labels = list(
        df_train['message']), list(df_train['label'])

    # --------------- Filtering with Naive Bayes method ---------------
    c_values = [0.2, 10, 100, 1000, 10000]
    best_c = 0
    nb_f_measure = 0
    best_nb = None

    for c in c_values:
        print()
        nb = NaiveBayes(
            documents=train_documents,
            labels=train_labels,
            debug=args.debug,
            c=c
        )

        # Validating
        print()
        log('Validating')
        this_nb_f_measure = filter(filter_obj=nb, df=df_validation.copy())

        if this_nb_f_measure > nb_f_measure:
            nb_f_measure = this_nb_f_measure
            best_c = c
            best_nb = nb

    log(
        f'Finished the validation for Naive Bayes and the best c value is {best_c}, taking in consideration the F-Measure of {nb_f_measure.f_measure()* 100:.4f}%.')
    # Testing
    print()

    log('Testing')
    filter(filter_obj=best_nb, df=df_test.copy())

    # --------------- Filtering with Perceptron ---------------
    t_values = [1, 10, 100, 1000, 10000]

    best_t = 0
    perceptron_f_measure = 0
    best_perceptron = None

    for t in t_values:
        print()
        perceptron = Perceptron(
            documents=train_documents,
            labels=train_labels,
            debug=args.debug,
            t=t
        )

        # Validating
        print()
        log('Validating')
        this_perceptron_f_measure = filter(
            filter_obj=nb, df=df_validation.copy())

        if this_perceptron_f_measure > perceptron_f_measure:
            perceptron_f_measure = this_perceptron_f_measure
            best_t = t
            best_perceptron = perceptron

    log(
        f'Finished the validation for Perceptron and the best t value is {best_t}, taking in consideration the F-Measure of {perceptron_f_measure.f_measure()* 100:.4f}%.')

    # Testing
    print()

    log('Testing')
    filter(filter_obj=best_perceptron, df=df_test.copy())
