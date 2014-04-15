#!/usr/bin/env python
import ftorrents.config
import ftorrents.downloader
import logging
logger = logging.getLogger("ftorrents")
logger.setLevel(logging.DEBUG)
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
