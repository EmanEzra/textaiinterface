from flask import Flask, request
# keras module for building LSTM
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
import keras.utils as ku
import string
import numpy as np

app = Flask(__name__)


@app.route('/home')
def home():
    return {'members': ['Hello World']}


@app.route('/input_layer', methods=['GET', 'POST'])
def split_text():
    print(request.get_json())
    text = request.get_json()['text']
    res = clean_text(text)
    input_sequences, total_words, word_dict = get_sequence_of_tokens([res])
    predictors, label, max_sequence_len = generate_padded_sequences(input_sequences, total_words)
    model = create_model(max_sequence_len, total_words)
    res = model.get_layer('embedding_layer').weights[0]
    print(word_dict)
    res = [[str(round(j.numpy(), 4)) for j in word_row] for word_row in res]
    res = [[word_dict[index + 1], index+1] + row for index, row in enumerate(res) if (index + 1) in word_dict.keys()]
    print(res)
    print(total_words)

    return {'members': res}


def get_sequence_of_tokens(corpus):
    # tokenization
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    r = {index: word for word, index in tokenizer.word_index.items()}
    # convert data to a token sequence
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words, r


def clean_text(txt):
    txt = "".join(t for t in txt if t not in string.punctuation).lower()
    txt = txt.encode("utf8").decode("ascii", 'ignore')
    return txt


def generate_padded_sequences(input_sequences, total_words):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len


def create_model(max_sequence_len, total_words):
    input_len = max_sequence_len - 1
    model = Sequential()
    # ----------Add Input Embedding Layer
    model.add(Embedding(total_words, 10, input_length=input_len, name='embedding_layer'))
    # ----------Add Hidden Layer 1 - LSTM Layer
    model.add(LSTM(100))
    model.add(Dropout(0.1))
    # ----------Add Output Layer
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model


if __name__ == '__main__':
    app.run(debug=True)
