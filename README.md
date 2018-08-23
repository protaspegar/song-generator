# Song Generator

A machine learning experiment to generate song lyrics

For now, it generates only lyrics (no melody) and only a very poor lyric :-(
It is mainly replicating an existing lyric without the less used words

There are a few things to improve:
- Find a better NN model
- Optimize hyperparameters
- Optmize the word tokenizer


The project is composed by 2 parts:

1. A lyric scrapper that gets all lyrics from a band from a website. Note that this may be against the site policy, so be careful.

2. A lyrics generator that uses the scrapped data as input for trainning.


## Scraper

This tool scraps a lyrics web site to extract lyrics from an artist and prepare it to be used by the ML model.

Some references:
* Source of lyrics: https://www.letras.mus.br
* Artist page: https://www.letras.mus.br/los-hermanos
* Song example: https://www.letras.mus.br/los-hermanos/47045/


### Docker

#### Setup environment

1. Download and install docker
2. Execute command `docker build -t scraper .`

This command will download and setup all dependencies, including Ubuntu, Python, Numpy, etc.
Please check Dockerfile to see the details of the environment


#### How to run

1. Execute the following command:

MacOS: `docker run --rm -v "$(pwd)":/app -w /app/app scraper sh -c 'python run.py'`

Windows: `docker run --rm -v /app -w /app/app scraper sh -c 'python run.py'`




## Generator

This tool receives a set of lyrics as input and generates new lyrics on the same style

Some references:
* One of the best references: https://machinelearningmastery.com/text-generation-lstm-recurrent-neural-networks-python-keras/
* Similar, but for word based: https://machinelearningmastery.com/how-to-develop-a-word-level-neural-language-model-in-keras/
* Keras tutorial Char-RNN: https://github.com/keras-team/keras/blob/master/examples/lstm_text_generation.py
* Keras word and char: https://github.com/mattdangerw/keras-text-generation
* Keras text pre-processing documentation: https://keras.io/preprocessing/text/
* Keras text pre-processing examples: http://www.orbifold.net/default/2017/01/10/embedding-and-tokenizer-in-keras/


### Docker

#### Setup environment

1. Download and install docker
2. Execute command `docker build -t generator .`

This command will download and setup all dependencies, including Ubuntu, Python, Numpy, etc.
Please check Dockerfile to see the details of the environment


#### How to run

1. Execute the following command:

MacOS: `docker run --rm -v "$(pwd)":/app -w /app/app generator sh -c 'python run.py'`

Windows: `docker run --rm -v /app -w /app/app generator sh -c 'python run.py'`
