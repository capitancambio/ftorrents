#!/usr/bin/env python
import ftorrents.config
import ftorrents.downloader
import logging
logger = logging.getLogger("ftorrents")
hand =  logging.FileHandler("/tmp/ftorrents.log")
logger.setLevel(logging.DEBUG)
hand.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(name)s] - %(levelname)s - %(message)s")
hand.setFormatter(formatter)
logger.addHandler(hand)
hand = logging.StreamHandler()
hand.setLevel(logging.DEBUG);
logger.addHandler(hand);

def main():
        try:
                ftorrents.downloader.new(ftorrents.config.load()).download()
        except RuntimeError as re:
                print re

if __name__ == "__main__" :
        main()
