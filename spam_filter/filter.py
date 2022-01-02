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

    return round(metrics_obj.f_measure(), 6), round(metrics_obj.precision(), 6)


def work_for_better_parameter(this_class, parameters: list, documents: list[list[str]], labels: list[int], df_validation: DataFrame, df_test: DataFrame, debug: bool = False):
    print()
    log(f'Finding the best parameter for {this_class.__name__}..')

    best_parameter = 0
    best_f_measure = 0
    best_precision = 0
    best_obj = None

    for parameter in parameters:
        log(f'Parameter: {parameter}, building object of {this_class.__name__}..')
        start = datetime.now()

        print()
        this_obj = this_class(
            documents=documents,
            labels=labels,
            debug=debug,
            parameter=parameter
        )
        log(f'Finalized in {datetime.now() - start} seconds.')

        # Validating
        print()
        log('Validating')
        this_f_measure, this_precision = filter(
            filter_obj=this_obj, df=df_validation.copy())

        if this_f_measure > (best_f_measure) or (this_f_measure == best_f_measure and this_precision > best_precision):
            best_f_measure = this_f_measure
            best_precision = this_precision
            best_parameter = parameter
            best_obj = this_obj

        log(f'Best parameter so far: {best_parameter}')

    log(
        f'Finished the validation for class and the best parameter value is {best_parameter}, taking in consideration the F-Measure of {best_f_measure* 100:.4f}%.')

    # Testing
    print()

    log('Testing')
    filter(filter_obj=best_obj, df=df_test.copy())
