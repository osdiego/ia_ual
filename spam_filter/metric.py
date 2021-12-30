from pandas import DataFrame

from log import log


class Metric:
    def __init__(self, df: DataFrame):
        self.tp = len(df.query('label == 1 and classified_as == 1'))
        self.fp = len(df.query('label == -1 and classified_as == 1'))
        self.tn = len(df.query('label == -1 and classified_as == -1'))
        self.fn = len(df.query('label == 1 and classified_as == -1'))

    def accuracy(self):
        return (self.tp + self.tn) / (self.tp + self.fp + self.tn + self.fn)

    def error_rate(self):
        return (self.fp + self.fn) / (self.tp + self.fp + self.tn + self.fn)

    def sensitivity(self):
        return (self.tp) / (self.tp + self.fn)

    def specificity(self):
        return (self.tn) / (self.tn + self.fp)

    def precision(self):
        return (self.tp) / (self.tp + self.fp)

    def recall(self):
        return (self.tp) / (self.tp + self.tn)

    def f_measure(self):
        p = self.precision()
        r = self.recall()

        return (2 * p * r) / (p + r)

    def print_me_metrics(self):
        log(f'Accuracy (acc) of: {self.accuracy()* 100:.4f}%')
        log(f'Error Rate (err) of: {self.error_rate()* 100:.4f}%')
        log(f'Sensitivity (sn) of: {self.sensitivity()* 100:.4f}%')
        log(f'Specificity (sp) of: {self.specificity()* 100:.4f}%')
        log(f'Precision (p) of: {self.precision()* 100:.4f}%')
        log(f'Recall (r) of: {self.recall()* 100:.4f}%')
        log(f'F-Measure (FM) of: {self.f_measure()* 100:.4f}%')
