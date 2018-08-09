# Generator

The lyrics Generator is an attempt to create new lyrics based on a set of lyrics used as input.
In the background, there is a word based LSTM text generator.

Note: *I've chosen to have it word based just because it seems easier (in my opinion) for a network to learn a sequence of words instead of learning a sequence of chars and them a sequence of words. But there is no technical background behind my choice. Anyway, this is just the first attempt and I can implement more fancy versions in the future.*

Each training pattern of the network is comprised of (T) time steps of one word (W) followed by one word output (Y). When creating these sequences, we slide this window along the whole input one word at a time, allowing each word a chance to be learned from the (T) words that preceded it (except the first (T) characters of course).

For starting (T) will be 5. Which means that we're going to have 5 words as input to predict 1 additional word.


In this readme file you will find the description of the main modules of this code.


## Run.py

This is the entry point of the code. To start the application, run this on the terminal

` docker run --rm -v "$(pwd)":/app -w /app/app scraper sh -c 'python run.py' `

This module initializes the logger and the Generator



## Generator.py

The generator is the main module. It reads the input data, defines the NN Model, trains, and predict new lyrics.
Of course, it doesn't do all of this by itself. But this is the module responsible by orchestrating the activities.