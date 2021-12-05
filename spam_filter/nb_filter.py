from datetime import datetime

from pandas import DataFrame

from naive_bayes import NaiveBayes


def nb_filter(documents: DataFrame, train_threshold: tuple[int], test_threshold: tuple[int], validation_threshold: tuple[int]) -> None:
    start = datetime.now()
    print(f'\nStarting nb_filter at {start}')

    # Training
    nb = NaiveBayes()

    train_dataset = documents[train_threshold[0]:train_threshold[1]]
    train_documents, train_labels = list(
        train_dataset['message']), list(train_dataset['label'])

    nb.train(train_documents, train_labels)

    # Testing
    test_dataset = documents[test_threshold[0]:test_threshold[1]]
    test_dataset['classified_as'] = None

    for index, row in test_dataset.iterrows():
        document = list(row['message'])
        test_dataset.loc[index, 'classified_as'] = nb.classify(document)

    test_accuracy = len(
        test_dataset[test_dataset.label == test_dataset.classified_as]) / len(test_dataset)
    print(
        f'\nThe test dataset was validated with {test_accuracy * 100:.4f}% of accuracy.')

    # Validating
    validation_dataset = documents[validation_threshold[0]:validation_threshold[1]]
    validation_dataset['classified_as'] = None

    for index, row in validation_dataset.iterrows():
        document = list(row['message'])
        validation_dataset.loc[index, 'classified_as'] = nb.classify(document)

    validation_accuracy = len(
        validation_dataset[validation_dataset.label == validation_dataset.classified_as]) / len(validation_dataset)
    print(
        f'\nThe validation dataset was validated with {validation_accuracy * 100:.4f}% of accuracy.')

    print(
        f'\nNaive Bayes filter finalized in {datetime.now() - start} seconds.')
