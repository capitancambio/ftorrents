#!/usr/bin/env python
import ftorrents.config
import ftorrents.downloader
import ftorrents.notifier
import logging

logger = logging.getLogger("ftorrents")
logger.setLevel(logging.DEBUG)
hand = logging.StreamHandler()
hand.setLevel(logging.DEBUG);
logger.addHandler(hand);

def main():
        try:
                downloads=ftorrents.downloader.new(ftorrents.config.load()).download()
                if len(downloads)>0:
                        ftorrents.notifier.notify(downloads)

        except RuntimeError as re:
                print re

if __name__ == "__main__" :
        main()
