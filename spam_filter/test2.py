from datetime import datetime
from naive_bayes import NaiveBayes
import pandas as pd
from pprint import pprint
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.ParserWarning)
warnings.simplefilter(
    action='ignore', category=pd.core.common.SettingWithCopyWarning)

print(datetime.now())

pd.set_option('display.max_colwidth', -1)
documents = pd.read_csv('documents.csv', sep=r'\t',
                        header=None)

documents.columns = ['label', 'message']

documents['message'] = documents['message'].apply(
    lambda document: document.lower())

documents['message'] = documents['message'].apply(
    lambda document: re.findall(r"[a-z0-9']+", document, re.IGNORECASE))

train_dataset = documents[0:3902]

nb = NaiveBayes()
train_documents, train_labels = list(
    train_dataset['message']), list(train_dataset['label'])

print('treinar')
nb.train(train_documents, train_labels)
# exit()

# 5574
# 70% = 0 to 3902 (not include)
# 15% = 3902 to 4739 (not include)
# 15% = 4739 to 5574 (not include)

test_dataset = documents[3902:4739]
test_dataset['classified_as'] = None
print(test_dataset)

for index, row in test_dataset.iterrows():
    document = list(row['message'])
    # print(document)
    test_dataset.loc[index, 'classified_as'] = nb.classify(document)

print(test_dataset)
print(len(test_dataset))

print(len(test_dataset.query('label == classified_as')))
print(len(test_dataset[test_dataset.label == test_dataset.classified_as]))

print(len(test_dataset['ham' == test_dataset.classified_as]))
print(len(test_dataset['spam' == test_dataset.classified_as]))
print(datetime.now())
