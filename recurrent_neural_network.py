import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, Embedding
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
from keras.preprocessing.text import Tokenizer

def sample(preds, temperature=1.0):
   preds = np.asarray(preds).astype('float64')
   preds = np.log(preds) / temperature
   exp_preds = np.exp(preds)
   preds = exp_preds / np.sum(exp_preds)
   probas = np.random.multinomial(1, preds, 1)
   return np.argmax(probas)

def generate_text(diversity, text, maxlen, word_id, id_word, model):
   sentence = 'Are you muslim'
   generated = ''

   x_pred = np.zeros((1, maxlen, len(text)))
   for t, char in enumerate(sentence.split(' ')):
      if char in word_id:
         x_pred[0, t, word_id[char]] = 1.0

      preds = model.predict(x_pred, verbose=0)[0]
      next_index = sample(preds, diversity)
      next_char = id_word[next_index]

      generated += next_char + ' '

   return generated

def train(x, y, chars, maxlen):
   model = Sequential()
   model.add(LSTM(128, input_shape=(maxlen, len(chars))))
   model.add(Dense(len(chars)))
   model.add(Activation('softmax'))

   optimizer = RMSprop(lr=0.01)
   model.compile(loss='categorical_crossentropy', optimizer=optimizer)

   filepath = 'weights.hdf5'
   checkpoint = ModelCheckpoint(filepath, monitor='loss',
                                 verbose=1, save_best_only=True,
                                 mode='min')
                              
   reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2,
                                 patience=1, min_lr=0.001)

   callbacks = [checkpoint, reduce_lr]

   model.fit(x, y, batch_size=128, epochs=100, callbacks=callbacks)

def output(text , maxlen, word_id, id_word, sentence):
   model = Sequential()
   model.add(LSTM(128, input_shape=(maxlen, len(text))))
   model.add(Dense(len(text)))
   model.add(Activation('softmax'))
   model.load_weights('weights.hdf5')

   diversity = 1.0
   generated = ''

   x_pred = np.zeros((1, maxlen, len(text)))
   for t, char in enumerate(sentence.split(' ')):
      if char in word_id:
         x_pred[0, t, word_id[char]] = 1.0

      preds = model.predict(x_pred, verbose=0)[0]
      next_index = sample(preds, diversity)
      next_char = id_word[next_index]

      generated += next_char + ' '
   return generated

def startup():
   temp = list()

   with open('training.txt', 'r') as f:
      for lines in f:
         for line in lines.split('\n'):
            if line != '':
               temp.append(line)

   lines = temp

   word_id = dict((w, i) for i, w in enumerate(lines))
   id_word = dict((i, w) for i, w in enumerate(lines))
   
   maxlen = 5

   # used if model needs to be trained
   # uncomment train line
   step = 3
   sentences = []
   next_chars = []
   for i in range(0, len(lines) - maxlen, step):
      sentences.append(lines[i : i + maxlen])
      next_chars.append(lines[i + maxlen])

   x = np.zeros((len(sentences), maxlen, len(lines)), dtype=np.bool)
   y = np.zeros((len(sentences), len(lines)), dtype=np.bool)
   for i, sentence in enumerate(sentences):
      for t, char in enumerate(sentence):
         x[i, t, word_id[char]] = 1
      y[i, word_id[next_chars[i]]] = 1

   # train(x, y, lines, maxlen)
   
   return lines, maxlen, word_id, id_word