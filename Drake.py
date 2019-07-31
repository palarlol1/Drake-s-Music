from tensorflow.keras import models
import numpy as np
import json

Drake = models.load_model("Drake.hdf5")
with open("char_map.json", 'r') as file:
    char_map = json.load(file)

reverse_map = {}
with open("decoder.json", 'r') as file:
    reverse_map = json.load(file)

seed = ('''yo what's goin on, this is drake and i'ma let you know
''')
text = seed.lower() + ""
song_length = 2500
sequence_length = 45
for i in range(song_length):
    pattern = text[len(text) - sequence_length:len(text)]
    x = [[]]
    for char in pattern:
        x[0].append([char_map[char]])
    x = np.array(x)
    x = x / float(len(char_map))
    next_char = Drake.predict_classes(x,verbose=0)
    index = next_char[0]
    text += reverse_map[str(index)]
    print(text)
