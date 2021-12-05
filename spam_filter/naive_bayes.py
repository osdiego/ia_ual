from numpy import log
import pandas as pd
from datetime import datetime


class NaiveBayes:
    def __init__(self, c=0.78) -> None:
        self.c = c
        self.b = 0
        # self.bag_of_words initialized in train method
        self.n = 0  # number of distinct words in all train documents
        # self.p initialized in train method

    def train(self, documents, labels) -> None:
        self.bag_of_words = set()

        for document in documents:
            for word in document:
                self.bag_of_words.add(word)

        self.bag_of_words = tuple(sorted(list(self.bag_of_words)))
        self.n = len(self.bag_of_words)

        m = len(labels)
        m_ham = labels.count('ham')
        m_spam = labels.count('spam')

        self.b = log(self.c) + log(m_ham) - log(m_spam)

        self.p = pd.DataFrame([[1 for i in range(self.n)],
                               [1 for i in range(self.n)]], columns=self.bag_of_words)

        # print(self.bag_of_words)
        # print(len(self.bag_of_words))
        # print(self.p)
        # exit()

        w_spam = self.n
        w_ham = self.n

        for document_id, document in enumerate(documents):
            if labels[document_id] == 'spam':
                for word in set(document):
                    occurrences = document.count(word)
                    self.p.loc[0, word] += occurrences
                    w_spam += occurrences

            else:  # == 'ham'
                for word in set(document):
                    occurrences = document.count(word)
                    self.p.loc[1, word] += occurrences
                    w_ham += occurrences

        # print(self.p)
        # self.p = self.p.apply(lambda row: row/2 if row.index == 0 else row/4)
        print(datetime.now())
        for word in self.bag_of_words:
            self.p.loc[0, word] = self.p.loc[0, word] / w_spam
            self.p.loc[1, word] = self.p.loc[1, word] / w_ham
        print(datetime.now())
        # print(self.p)
        # print(w_spam, w_ham)

    def classify(self, document) -> str:
        t = - self.b

        # for word in self.bag_of_words:
        for word in set(document):
            if word in self.bag_of_words:
                t += document.count(word) * \
                    (log(self.p.loc[0, word]) - log(self.p.loc[1, word]))

        return 'spam' if t > 0 else 'ham'
