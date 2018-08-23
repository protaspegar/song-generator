import logging
import numpy
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils


class TextProcessor:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.tokenizer = Tokenizer(num_words=500, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t')
        self.sequence = []
        self.dictionary = []
        self.inv_dictionary = []
        self.wordsOnInput = 50


    def ProcessRawInput(self, rawInputText):
        inputText = rawInputText.lower() #convert everything to lower case
        inputText = self.ReplaceAccentuation(inputText)
        inputText = self.AddSpaceToLineBreak(inputText)

        self.tokenizer.fit_on_texts([inputText])

        self.sequence = self.tokenizer.texts_to_sequences([inputText])[0]
        #print(self.sequence)
        self.dictionary = self.tokenizer.word_index
        self.inv_dictionary = {v: k for k, v in self.dictionary.items()}
        #print(self.dictionary)

        print("Total words: ", len(self.sequence))
        print("Total vocabulary: ", len(self.tokenizer.word_counts))
        print("Como é que vai você: ", self.tokenizer.texts_to_sequences(["Como é que vai você"]))

        return self.sequence, self.dictionary

    def ReplaceAccentuation(self, inputText):
        inputText = inputText.replace("à", "a")
        inputText = inputText.replace("ã", "a")
        inputText = inputText.replace("á", "a")
        inputText = inputText.replace("â", "a")

        inputText = inputText.replace("ç", "c")

        inputText = inputText.replace("é", "eh") #This is special for portuguese language
        inputText = inputText.replace("è", "e") 
        inputText = inputText.replace("ê", "e") 

        inputText = inputText.replace("í", "i")
        inputText = inputText.replace("ì", "i")

        inputText = inputText.replace("ó", "o")
        inputText = inputText.replace("ô", "o")

        inputText = inputText.replace("ú", "u")
        inputText = inputText.replace("ù", "u")

        return inputText

    def AddSpaceToLineBreak(self, rawInputText):
        # This method is needed because the tokenizer uses an empty space to split the words
        inputText = rawInputText.replace("\n", " \n ")
        return inputText

    def PrepareTrainingDataset(self):
        # Prepare the dataset of input to output pairs encoded as integers
        seq_length = self.wordsOnInput
        n_words = len(self.sequence)
        sequencesX = []
        sequencesY = []
        for i in range(0, n_words - seq_length, 1):
            seq_in = self.sequence[i:i + seq_length]
            seq_out = self.sequence[i + seq_length]
            sequencesX.append(seq_in)
            sequencesY.append([seq_out]) #seq_out is only one word, therefore we need the [] to force an array
        n_patterns = len(sequencesX)
        print("Total Patterns: ", n_patterns)
        return sequencesX, sequencesY

    def ReshapeInputSequences(self, sequencesX):
        # We need to rescale the integers to the range 0-to-1 to make the patterns easier to learn 
        # by the LSTM network that uses the sigmoid activation function by default.
        # reshape X to be [samples, time steps, features]
        
        # dataX = numpy.reshape(sequencesX, (len(sequencesX), self.wordsOnInput, 1))
        # dataX = self.NormalizeInputData(dataX)

        dataX = numpy.array(sequencesX)

        return dataX

    def NormalizeInputData(self, dataX):
        # normalize
        n_vocab = len(self.tokenizer.word_counts)
        dataX = dataX / float(n_vocab)
        return dataX


    def EncodeOutputSequences(self, sequencesY):
        # one hot encode the output variable
        dataY = np_utils.to_categorical(sequencesY, len(self.dictionary)+1)
        return dataY

    def ConvertIndexToWord(self, outputIndex):
        return self.inv_dictionary[outputIndex]

    def ConvertTextToSequence(self, text):
        return self.tokenizer.texts_to_sequences([text])[0]


