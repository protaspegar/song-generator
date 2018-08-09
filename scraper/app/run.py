import logging
import logging.handlers
import scraper

def setupLogger():
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    logFileHandler = logging.handlers.TimedRotatingFileHandler('Logs/Scraper',  when='midnight')
    logFileHandler.suffix = '%Y_%m_%d.log'
    logFileHandler.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logFileHandler.setFormatter(formatter)
    log.addHandler(logFileHandler)


def main():
    setupLogger()

    scrp = scraper.Scraper()
    scrp.Start()
    scrp.SaveToFile()
    
    

if __name__ == '__main__':
    main()