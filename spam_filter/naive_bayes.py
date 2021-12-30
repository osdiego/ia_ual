from numpy import log as np_log

from log import log, log_debug


class NaiveBayes:
    def __init__(self, documents: list[list[str]], labels: list[int], parameter: float = 0.2, debug: bool = False) -> None:
        log(__name__)
        self.c = parameter
        self.documents = documents
        self.labels = labels
        self.b = 0
        self.all_document_words = ()  # initialized in train method
        self.n = 0  # number of distinct words in all train documents
        self.p = {}  # initialized in train method
        self.debug = debug
        self.train()

    def train(self) -> None:
        log_debug('training', self.debug)

        self.all_document_words = set()

        for document in self.documents:
            for word in document:
                self.all_document_words.add(word)

        self.all_document_words = tuple(sorted(list(self.all_document_words)))
        self.n = len(self.all_document_words)

        m_ham = self.labels.count(-1)
        m_spam = self.labels.count(1)

        self.b = np_log(self.c) + np_log(m_ham) - np_log(m_spam)

        self.p = {
            'spam': dict(zip(self.all_document_words, (1 for i in range(self.n)))),
            'ham': dict(zip(self.all_document_words, (1 for i in range(self.n))))
        }

        w_spam = self.n
        w_ham = self.n

        for document_id, document in enumerate(self.documents):
            if self.labels[document_id] == 1:
                for word in set(document):
                    occurrences = document.count(word)
                    self.p['spam'][word] += occurrences
                    w_spam += occurrences

            else:  # == 'ham'
                for word in set(document):
                    occurrences = document.count(word)
                    self.p['ham'][word] += occurrences
                    w_ham += occurrences

        self.p['spam'] = {k: v/w_spam for k, v in self.p['spam'].items()}
        self.p['ham'] = {k: v/w_ham for k, v in self.p['ham'].items()}

    def classify(self, document: list[str]) -> str:
        t = -self.b

        for word in set(document):
            if word in self.all_document_words:
                t += document.count(word) * \
                    (np_log(self.p['spam'][word]) -
                     np_log(self.p['ham'][word]))

        return 1 if t > 0 else -1
