import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import keras
import random
import pandas as pd
import json



stoplist = set("""for a of what can about don't these them any much each well any these
               doesn't that's when show series character characters how o y e 
               get up out then do only we it's which there because even neither 
               nor my were la the and to in is that i you was it this her with but 
               their its not while they are like very as who be an his her she he him just 
               really on it\'s de que no or are anime have all so has at from by more 
               some one me if would other also into it's will being your than most many
               few none where does while through way such think had good story make say me
               our own why know time off both first around may through things something thing give 
               want many ? i I as is it""".split())
import pickle

# try:
#    with open("data.pickle", "rb") as f:
#        words, labels, training, output = pickle.load(f)
class nlp:

    def __init__(self):
        self.raw_data = pd.read_json("intents.json")

        with open("intents.json") as file:
            data = file.read()
            print(data)

        #raw_data.head()

        self.words = []  # list of all words in patterns
        self.labels = []  # list of possible tags
        self.docs_x = []  # list of words in each tag
        self.docs_y = []  # corresponding tag to each word

        for intent in self.raw_data["intents"]:
            for pattern in intent["patterns"]:
                # stem the patterns
                wrds = nltk.word_tokenize(pattern)  # returns a list of tokenized words
                self.words.extend(wrds)
                self.docs_x.append(pattern)
                self.docs_y.append(intent["tag"])

                if intent["tag"] not in self.labels:
                    self.labels.append(intent["tag"])

        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in stoplist]
        self.words = sorted(list(set(self.words)))

        self.labels = sorted(self.labels)

        self.training = []
        self.output = []

        out_empty = [0 for _ in range(len(self.labels))]

        for x, doc in enumerate(self.docs_x):
            bag = []
            # print(doc)
            # wrds = [stemmer.stem(w) for w in doc]
            wrd = stemmer.stem(doc)

            for w in self.words:
                if w in wrd:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[self.labels.index(self.docs_y[x])] = 1

            self.training.append(bag)
            self.output.append(output_row)

        self.training = np.array(self.training)
        self.output = np.array(self.output)

        # catches 'i' in 'hi' but okay for now...
        #Dependencies
        import keras
        from keras.models import Sequential
        from keras.layers import Dense
        from keras.layers import Flatten
        from keras.layers import LSTM
        from keras.layers import Activation

        # Neural network 1
        self.model = Sequential()
        self.model.add(Dense(50, input_dim=len(self.training[0]), activation='relu'))
        self.model.add(Dense(35, activation='relu'))
        self.model.add(Dense(25, activation='relu'))
        #model.add(Flatten())
        self.model.add(Dense(len(self.output[0]), activation='softmax'))



        # Neural network 2
        #self.training = self.training.reshape(self.training.shape[0], self.training.shape[1], 1)
        # print(self.training.shape)

        #self.model = Sequential()
        #self.model.add(LSTM(30, input_shape=(self.training.shape[1], 1), return_sequences=True))
        #self.model.add(LSTM(30, input_shape=(self.training.shape[1], 1), return_sequences=False))
        #self.model.add(LSTM(8, input_shape=len(self.training[0]), return_sequences=True))
        #model.add(Dropout(0.5))
        #self.model.add(Dense(30, activation='softmax'))
        #self.model.add(Dense(len(self.output[0]), activation='softmax'))
        #self.model.add(Activation('sigmoid'))


        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(self.training, self.output, epochs=7, batch_size=8)
        self.model.save("model.tflearn")

    # function to process input
    def bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1
        return np.array(bag)


    # function to chat with bot
    def chat(self):
        print("Start talking with the bot!")
        while True:
            inp = input("You: ")
            if inp.lower() == "quit":
                break
            inp_pr = np.array([self.bag_of_words(inp, self.words)])
            results = self.model.predict(inp_pr)[0]

            results_index = np.argmax(results)  # index of greatest value in list
            tag = self.labels[results_index]  # gives class(label) of message

            if results[results_index] > 0.5:

                for tg in self.raw_data["intents"]:
                    if tg['tag'] == tag:
                        responses = tg['responses']

                print("RoBot: ", random.choice(responses))

            else:
                print("Sorry I didnt understand")
