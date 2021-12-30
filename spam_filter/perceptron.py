from numpy import dot

from log import log, log_debug


class Perceptron:
    def __init__(self, documents: list[list[str]], labels: list[int], parameter: int = 10, debug: bool = False) -> None:
        log(__name__)
        self.documents = documents
        self.labels = labels
        self.t = parameter
        self.debug = debug
        self.prepare()
        self.train()

    def prepare(self) -> None:
        log_debug('preparing lexicon', self.debug)
        # Preparing lexicon
        self.all_document_words = set()

        for document in self.documents:
            for word in document:
                self.all_document_words.add(word)

        self.all_document_words = tuple(sorted(list(self.all_document_words)))

        # Preparing document vectors
        self.all_document_vectors = []

        for document in self.documents:
            self.all_document_vectors.append(
                [document.count(word) for word in self.all_document_words]
            )

    def train(self):
        log_debug('training', self.debug)

        self.theta = [0 for _ in range(len(self.all_document_words))]
        self.theta_0 = 0

        for epoch in range(1, self.t + 1):
            log_debug(f'epoch = {epoch}', self.debug)
            for vector, label in zip(self.all_document_vectors, self.labels):
                if label * (dot(self.theta, vector) + self.theta_0) <= 0:
                    label_x_vector = [label * v for v in vector]
                    self.theta = [
                        x + y for x, y in zip(self.theta, label_x_vector)
                    ]
                    self.theta_0 += label

    def classify(self, document: list[str]):
        vector = [document.count(word) for word in self.all_document_words]

        return 1 if (dot(self.theta, vector) + self.theta_0) > 0 else -1
