import os
import re

import matplotlib.pyplot as plt
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.naive_bayes import MultinomialNB

CSV_FILE_NAME = 'spam_or_not_spam.csv'
EMAIL_COLUMN_NAME = 'email'
LABEL_COLUMN_NAME = 'label'

NUMBER_OF_FOLDS = 5

VOCAB_SIZE = 10000
TRUNC_TYPE = "post"
PAD_TYPE = "post"
OOV_TOK = "<OOV>"

if __name__ == '__main__':
    # Não exibe mensagem de aviso do TensorFlow
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    print('Lendo arquivo CSV')

    file_path = os.path.join(os.path.dirname(__file__), CSV_FILE_NAME)
    df = pd.read_csv(file_path)

    print('Processando conjunto de dados')

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

    confusion_matrices = []
    accuracies = []
    stratified_kfold = StratifiedKFold(n_splits=NUMBER_OF_FOLDS, shuffle=True, random_state=42)

    for i, (train_idx, val_idx) in enumerate(stratified_kfold.split(X, y)):
        print(f'Treinando fold {i + 1}/{NUMBER_OF_FOLDS}')

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

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

        classifier = MultinomialNB()
        classifier.fit(X_train, y_train)

        print(f'Realizando testes do fold {i + 1}/{NUMBER_OF_FOLDS}')

        y_pred = classifier.predict(X_val)

        print('Calculando métricas')
        confusion_matrices.append(confusion_matrix(y_val, y_pred))
        accuracies.append(accuracy_score(y_val, y_pred))

    print('Resultados dos testes')

    for i, acc in enumerate(accuracies):
        print(f'Acurácia do Teste {i + 1}: {acc}')
    else:
        print('Acurácia média: ', np.average(accuracies))

    for i, cm in enumerate(confusion_matrices):
        disp = ConfusionMatrixDisplay(cm)
        disp.plot()
        plt.title(f'Matriz de Confusão do Fold {i + 1}/{NUMBER_OF_FOLDS}')
        plt.xlabel('Classe Predita')
        plt.ylabel('Classe Verdadeira')
    else:
        disp = ConfusionMatrixDisplay(np.mean(confusion_matrices, axis=0))
        disp.plot(values_format='.2f')
        plt.title('Matriz de Confusão Média')
        plt.xlabel('Classe Predita')
        plt.ylabel('Classe Verdadeira')

    plt.show()