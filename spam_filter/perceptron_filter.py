from numpy import dot


class Perceptron:
    def __init__(self, documents: list[list[str]], labels: list[str], t: int = 10) -> None:
        self.n = len(documents)
        self.documents = documents
        self.labels = [-1 if label == 'ham' else 1 for label in labels]
        self.t = t
        self.prepare()

    def prepare(self) -> None:
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
        self.theta = [0 for _ in range(self.n)]
        self.theta_0 = 0

        for _ in self.t:
            for vector, label in zip(self.all_document_vectors, self.labels):
                if label * (dot(self.theta, vector) + self.theta_0) <= 0:
                    label_x_vector = [label * v for v in vector]
                    self.theta = [
                        x + y for x, y in zip(self.theta, label_x_vector)
                    ]
                    self.theta_0 += label

    def classifier(self, document: list[str]):
        vector = [document.count(word) for word in self.all_document_words]

        if (dot(self.theta, vector) + self.theta_0) <= 0:
            return 'ham'
        else:
            return 'spam'
