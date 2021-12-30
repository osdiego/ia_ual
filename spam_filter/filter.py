from datetime import datetime

from pandas import DataFrame

from log import log
from metric import Metric


def filter(filter_obj, df: DataFrame) -> None:
    start = datetime.now()
    log(f'Starting {type(filter_obj).__name__} filter..')

    for index, row in df.iterrows():
        document = list(row['message'])
        df.loc[index, 'classified_as'] = filter_obj.classify(document)

    metrics_obj = Metric(df)
    metrics_obj.print_me_metrics()

    print()
    log(f'{type(filter_obj).__name__} filter finalized in {datetime.now() - start} seconds.')

    return metrics_obj.f_measure()


def work_for_better_parameter(parameters: list, documents: list[list[str]], labels: list[int], df_validation: DataFrame, df_test: DataFrame, debug: bool = False):
    log('Finding the best parameter for it..')

    best_parameter = 0
    best_f_measure = 0
    best_obj = None

    for parameter in parameters:
        print()
        this_obj = Perceptron(
            documents=documents,
            labels=labels,
            debug=debug,
            parameter=parameter
        )

        # Validating
        print()
        log('Validating')
        this_f_measure = filter(
            filter_obj=this_obj, df=df.copy())

        if this_f_measure > perceptron_f_measure:
            perceptron_f_measure = this_f_measure
            best_parameter = parameter
            best_obj = this_obj

    log(
        f'Finished the validation for Perceptron and the best t value is {best_parameter}, taking in consideration the F-Measure of {best_f_measure.f_measure()* 100:.4f}%.')

    # Testing
    print()

    log('Testing')
    filter(filter_obj=best_obj, df=df_test.copy())
