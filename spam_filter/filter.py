from datetime import datetime

from pandas import DataFrame

from log import log
from metric import Metric


def filter(filter_obj, df_test: DataFrame, df_validation: DataFrame) -> None:
    start = datetime.now()
    log(f'Starting {type(filter_obj).__name__} filter..')

    # Testing
    print()
    log('Testing')

    for index, row in df_test.iterrows():
        document = list(row['message'])
        df_test.loc[index, 'classified_as'] = filter_obj.classify(document)

    test_metrics = Metric(df_test)
    test_metrics.print_me_metrics()

    # Validating
    print()
    log('Validating')

    for index, row in df_validation.iterrows():
        document = list(row['message'])
        df_validation.loc[index,
                          'classified_as'] = filter_obj.classify(document)

    validation_metrics = Metric(df_validation)
    validation_metrics.print_me_metrics()

    print()
    log(f'{type(filter_obj).__name__} filter finalized in {datetime.now() - start} seconds.')
