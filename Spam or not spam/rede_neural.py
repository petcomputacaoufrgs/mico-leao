import os
import re

from keras.metrics import BinaryAccuracy
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
import tensorflow as tf
from tensorflow import keras

CSV_FILE_NAME = 'spam_or_not_spam.csv'
EMAIL_COLUMN_NAME = 'email'
LABEL_COLUMN_NAME = 'label'

NUMBER_OF_FOLDS = 5

VOCAB_SIZE = 10000
TRUNC_TYPE = "post"
PAD_TYPE = "post"
OOV_TOK = "<OOV>"

EMBEDDING_DIM = 16
HIDDEN_LAYER_DIM = 24
LEARNING_RATE = 0.001
NUMBER_OF_EPOCHS = 30
BATCH_SIZE = 32

CERTAINTY_THRESHOLD = 0.5

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

    histories = []
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

        tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token=OOV_TOK)
        tokenizer.fit_on_texts(X_train)

        X_train = tokenizer.texts_to_sequences(np.array(X_train))
        X_train = pad_sequences(X_train, truncating=TRUNC_TYPE, padding=PAD_TYPE)

        max_length = len(X_train[0])

        X_val = tokenizer.texts_to_sequences(np.array(X_val))
        X_val = pad_sequences(X_val, padding=PAD_TYPE, truncating=TRUNC_TYPE, maxlen=max_length)

        model = keras.Sequential([
            keras.layers.Embedding(VOCAB_SIZE, EMBEDDING_DIM, input_length=max_length),
            keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(HIDDEN_LAYER_DIM, activation='relu'),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(loss='binary_crossentropy',
                      optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                      metrics=[BinaryAccuracy()])

        history = model.fit(X_train,
                            y_train,
                            verbose=1,
                            epochs=NUMBER_OF_EPOCHS,
                            batch_size=BATCH_SIZE,
                            validation_data=(X_val, y_val))
        
        histories.append(history)
    
        print()
        print(f'Realizando testes do fold {i + 1}/{NUMBER_OF_FOLDS}')

        y_pred = (model.predict(X_val, verbose=1) > CERTAINTY_THRESHOLD).astype('int32')

        print()
        print('Calculando métricas')
        confusion_matrices.append(confusion_matrix(y_val, y_pred))
        accuracies.append(accuracy_score(y_val, y_pred))

    print('Resultados dos testes')
    
    for i, acc in enumerate(accuracies):
        print(f'Acurácia do Teste {i + 1}: {acc}')
    else:
        print('Acurácia média: ', np.average(accuracies))

    for i, hist in enumerate(histories):
        plt.figure()
        plt.plot(hist.history['binary_accuracy'])
        plt.plot(hist.history['val_binary_accuracy'])
        plt.title(f'Curva de Aprendizagem do Fold {i + 1}/{NUMBER_OF_FOLDS}')
        plt.xlabel('Épocas')
        plt.ylabel('Acurácia')
        plt.legend(['Conj. Treinamento', 'Conj. Validação'])

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