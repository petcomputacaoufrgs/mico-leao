import os
import re

import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB

CSV_FILE_NAME = 'spam_or_not_spam.csv'
EMAIL_COLUMN_NAME = 'email'
LABEL_COLUMN_NAME = 'label'

VOCAB_SIZE = 10000
TRUNC_TYPE = "post"
PAD_TYPE = "post"
OOV_TOK = "<OOV>"

EMBEDDING_DIM = 16
HIDDEN_LAYER_DIM = 24
LEARNING_RATE = 0.001
NUMBER_OF_EPOCHS = 30

CERTAINTY_THRESHOLD = 0.5

def plot_graphs(history, string):
    plt.plot(history.history[string])
    plt.plot(history.history['val_' + string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.legend([string, 'val_' + string])
    plt.show()

if __name__ == '__main__':
    file_path = os.path.join(os.path.dirname(__file__), CSV_FILE_NAME)
    df = pd.read_csv(file_path)

    df = df.drop_duplicates().dropna()

    X = df[EMAIL_COLUMN_NAME]
    y = df[LABEL_COLUMN_NAME]

    X = X.apply(lambda message: nltk.word_tokenize(message))
    X = X.apply(lambda token_list: [re.sub(r'[^A-Za-z]', ' ', token).lower() for token in token_list])

    stemmer = PorterStemmer()
    nltk.download('stopwords', quiet=True)
    stopwords = stopwords.words('english')

    X = X.apply(lambda token_list: [token for token in token_list if token not in stopwords])
    X = X.apply(lambda token_list: [stemmer.stem(token) for token in token_list])
    X = X.apply(lambda x: ' '.join(x))

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, stratify=y_train)

    train_ham_count = len(y_train[y_train == 0])
    train_spam_count = len(y_train[y_train == 1])
    oversampling_factor = train_ham_count // train_spam_count

    train = pd.DataFrame({EMAIL_COLUMN_NAME: X_train,
                          LABEL_COLUMN_NAME: y_train})
    
    train_ham = train[train[LABEL_COLUMN_NAME] == 0]
    train_spam = train[train[LABEL_COLUMN_NAME] == 1].sample(n=train_spam_count * oversampling_factor,
                                                             replace=True)

    train = pd.concat([train_ham, train_spam])

    X_train = train[EMAIL_COLUMN_NAME]
    y_train = train[LABEL_COLUMN_NAME]

    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    X_val = vectorizer.transform(X_val)
    X_test = vectorizer.transform(X_test)

    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)

    y_pred = classifier.predict(X_test)

    print('Acurácia: ', accuracy_score(y_test, y_pred))
    
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()