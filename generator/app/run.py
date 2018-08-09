import logging
import logging.handlers
import generator

def setupLogger():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    logFileHandler = logging.handlers.TimedRotatingFileHandler('Logs/Generator',  when='midnight')
    logFileHandler.suffix = '%Y_%m_%d.log'
    logFileHandler.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFileHandler.setFormatter(formatter)
    log.addHandler(logFileHandler)


def main():
    setupLogger()

    gen = generator.Generator()
    gen.Start()
    
    

if __name__ == '__main__':
    main()