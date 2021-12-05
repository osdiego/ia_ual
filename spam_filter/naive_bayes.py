from numpy import log


class NaiveBayes:
    def __init__(self, c: float = 0.2) -> None:
        self.c = c
        self.b = 0
        # self.all_document_words initialized in train method
        self.n = 0  # number of distinct words in all train documents
        # self.p initialized in train method

    def train(self, documents: list[list[str]], labels: list[str]) -> None:
        self.all_document_words = set()

        for document in documents:
            for word in document:
                self.all_document_words.add(word)

        self.all_document_words = tuple(sorted(list(self.all_document_words)))
        self.n = len(self.all_document_words)

        m_ham = labels.count('ham')
        m_spam = labels.count('spam')

        self.b = log(self.c) + log(m_ham) - log(m_spam)

        self.p = {
            'spam': dict(zip(self.all_document_words, (1 for i in range(self.n)))),
            'ham': dict(zip(self.all_document_words, (1 for i in range(self.n))))
        }

        w_spam = self.n
        w_ham = self.n

        for document_id, document in enumerate(documents):
            if labels[document_id] == 'spam':
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
                    (log(self.p['spam'][word]) - log(self.p['ham'][word]))

        return 'spam' if t > 0 else 'ham'
