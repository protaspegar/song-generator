import logging
import textprocessor
import numpy
from pathlib import Path
from random import randint, random

from keras.models import Sequential
from keras.layers import Embedding
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint


class Generator:
    def __init__(self):
        self.log = logging.getLogger(__name__)

        self.inputFilePath = 'Input/los-hermanos.txt'
        self.inputRawText = ""
        self.dictionary = None
        self.dataX = None
        self.dataY = None
        self.model = None

        self.epochs = 50 #5
        self.batch_size = 128
        self.generator_randomization = 0.1
        self.modelFilename = "Model/latest_v2.hdf5"


    def Start(self):
        self.log.info('Starting generator...')

        self.ReadInputFile()
        self.PreProcessInput()
        self.DefineModel()
        self.LoadTrainedModel()
        self.Train()
        self.GenerateNewText()

        self.log.info('Generator finished!')


    def ReadInputFile(self):
        self.log.info('Reading input file...')

        inputFile = open(self.inputFilePath, "r", encoding="utf-8")
        content = inputFile.read()
        inputFile.close()
        self.inputRawText = content


    def PreProcessInput(self):
        self.log.info('Pre-processing input data...')

        txtProc = textprocessor.TextProcessor()
        sequence, self.dictionary = txtProc.ProcessRawInput(self.inputRawText)
        sequencesX, sequencesY = txtProc.PrepareTrainingDataset()
        self.dataX = txtProc.ReshapeInputSequences(sequencesX)
        self.dataY = txtProc.EncodeOutputSequences(sequencesY)
        self.txtProcessor = txtProc


    def DefineModel(self):
        self.log.info('Loading LSTM model...')

        vocab_size = len(self.dictionary) + 1

        model = Sequential()
        model.add(Embedding(vocab_size, 100, input_length=self.dataX.shape[1])) #using 100 as a fixed embedding vector size
        #model.add(Embedding(vocab_size, self.dataX.shape[0], input_length=self.dataX.shape[1]))
        model.add(LSTM(512, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(512))
        model.add(Dropout(0.2))
        model.add(Dense(100))
        #model.add(Dense(100, activation='relu')) #do we need this relu layer?
        model.add(Dense(vocab_size, activation='softmax'))
        #model.add(Dense(self.dataY.shape[1], activation='softmax'))
        print(model.summary())

        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        self.model = model


    def Train(self):
        self.log.info('Training model...')

        # define the checkpoint
        # filepath="Model/weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
        filepath="Model/latest_v2.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        self.model.fit(self.dataX, self.dataY, epochs=self.epochs, batch_size=self.batch_size, callbacks=callbacks_list)


    def LoadTrainedModel(self):
        # load the network weights

        previouslySavedModelFile = Path(self.modelFilename)
        if previouslySavedModelFile.is_file():
            self.model.load_weights(self.modelFilename)
            self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            self.log.info('Loaded previously trained weights')



    def GenerateNewText(self):
        self.log.info('Generating new data...')

        seedText = self.ChooseRandomTextSeed()
        seedSequence = self.txtProcessor.ConvertTextToSequence(seedText)

        print("Seed: ", seedText)

        generatedText = ""

        # generate words
        for i in range(100):
            # x = self.txtProcessor.NormalizeInputData(seedSequence)
            x = numpy.array([seedSequence])
            #print("Input shape: ",x.shape)
            index = self.PredictClass(x) #self.model.predict_classes(x, verbose=0)[0]
            resultWord = self.txtProcessor.ConvertIndexToWord(index)
            generatedText += resultWord + " "
            # print("New: ", index, " - ", resultWord)
            seedSequence.append(index)
            #print(seedSequence)
            seedSequence = seedSequence[1:len(seedSequence)]

            

        print("===== DONE =====")
        print(generatedText)


    def PredictClass(self, inputText):
        prediction = self.model.predict(inputText, verbose=0)
        predicted_index = numpy.argmax(prediction)

        if (random() < self.generator_randomization):
            
            prediction[0][predicted_index] = 0.0
            predicted_index = numpy.argmax(prediction)

        return predicted_index


    def ChooseRandomTextSeed(self):
        seedSequence = self.dataX[randint(0,len(self.dataX))]
        seedText = ""
        for index in seedSequence:
            word = self.txtProcessor.ConvertIndexToWord(index)
            seedText += word + " "

        return seedText


