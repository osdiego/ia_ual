
def perceptron(todos os vetores dos documentos, todas as labels, n de documentos, épocas):
    teta = vetor a 0 com n de palavras do lexico
    teta0 = 0

    for epoca in epocas:
        for documento in documentos:
            if label do documento * ((teta * vetor de frequencias do documento) + teta0) <= 0:
                teta = teta + (label do documento * vetor de frequencias do documento)
                teta0 = teta0 + label do documento

    return teta, teta0


def classificador(vetor de frequencias do documento, teta, teta0):
    if (teta * vetor de frequencias do documento) + teta0 <= 0:
        return 'spam'
    else:
        return 'ham'
