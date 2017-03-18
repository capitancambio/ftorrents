ftorrents
=========
[![Build Status](https://travis-ci.org/capitancambio/ftorrents.svg)](https://travis-ci.org/capitancambio/ftorrents) [![Coverage Status](https://coveralls.io/repos/capitancambio/ftorrents/badge.png)](https://coveralls.io/r/capitancambio/ftorrents)

ftorrents is a small program that fetches the latest torrent files from [showrss.info](http://showrss.info). To configure it just run it one time to generate the configuration file, then edit the file adding the rss url. Make sure that you have generated the url including namespaces and disallowing magnet links. 

The downloaded files will be stored in ```~/.ftorrents/torrent_files```, or in the folder indicated in the configuration file.

*# Prerequisites
Library _libyaml_
  MAC: `brew install libyaml`
  Linux: `apt-get install libyaml`
*# Install
  `python setup.py install`
*# Configuration
  You'll need an account on showRSS to create the URL with no magnets and namespaces.
  Run once `./ftorrents.sh` and open the file `~/.ftorrents/cnf.yml` and set your RSS URL. 
