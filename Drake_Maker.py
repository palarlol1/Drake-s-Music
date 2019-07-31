#File Imports
import json
import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.preprocessing import OneHotEncoder

text = open('song_lyrics.txt').read()

chars = list(set(text))

char_map = {}

for char in chars:
    char_map[char] = ord(char)

with open("char_map.json", 'w+') as file:
    json.dump(char_map, file)

sequence_length = 45
X = []
y = []
for i in range(0, len(text) - sequence_length):
    input = text[i:i+sequence_length]
    output = text[i+sequence_length]
    X.append([char_map[char] for char in input])
    y.append([output])

X = numpy.reshape(X,(len(X), sequence_length, 1))
X = X/float(len(char_map))
encoder = OneHotEncoder(handle_unknown='ignore')
y = encoder.fit_transform(y).toarray()

i = 0
decoder = {}
for item in encoder.get_feature_names():
    decoder[i] = item[3]
    i+=1
with open('decoder.json', 'w+') as decoder_file:
    json.dump(decoder,decoder_file)
Drake = Sequential()
Drake.add(LSTM(300, input_shape=(X.shape[1], X.shape[2])))
Drake.add(Dropout(.19))
Drake.add(Dense(y.shape[1], activation="softmax")) #Output is set to the number of chars we have to work with.
Drake.compile(loss="categorical_crossentropy", optimizer='adam')
filepath="models//weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
Drake.fit(X, y, epochs = 100, batch_size=15,callbacks=callbacks_list)
Drake.save("Drake.h5")
