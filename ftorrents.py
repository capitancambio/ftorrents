#!/usr/bin/python
import urllib2
from StringIO import StringIO
import gzip
import pickle
import pynotify
import feedparser
import gtk
import os

import logging
#Credenciales showrss
#ftorrents
#ftorrents
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

class Config:

        def __init__(self):
                self.cache_file='/home/javi/.ftorrent/downloads'
                self.rss_url='http://showrss.info/rss.php?user_id=116775&hd=null&proper=null&namespaces=true&magnets=false'
                self.download_dir="/home/javi/src/ftorrents/torrent_files2/"


class TorrentDowner:
        def __init__(self,conf):
                self.conf=conf

        def openTransmission(self,n,action):
                assert action == "default"
                try:
                        os.popen2("transmission-gtk")
                        logging.getLogger("ftorrents").debug("Transmision open!")	
                except Exception as err:
                        logging.getLogger("ftorrents").warning(err)

                n.close()
                gtk.main_quit()

        def closeLoop(self,n):
                print "close loop..."
                logging.getLogger("ftorrents").debug("closing without openining transmission")	
                n.close()
                gtk.main_quit()


        def sendMessage(self,msg):
                pynotify.init("Ftorrents")
                notice = pynotify.Notification("Ftorrents", msg)
                notice.add_action("default", "Open Transmission", self.openTransmission)
                notice.connect("closed",self.closeLoop)
                notice.set_urgency(pynotify.URGENCY_LOW)
                try:
                        notice.show()
                        gtk.main()

                except Exception as err:
                        logging.getLogger("ftorrents").warning(err)	
                pass

        
        def getTorrents(self):
                logging.getLogger("ftorrents").debug("Starting to download torrents")
                #config
                #DOWN_DIR="/tmp/"
                episodes=FeedLoader(self.conf.rss_url).load()
                fDowns=open(self.conf.cache_file,'r')
                #gotchas=pickle.load(fDowns)
                gotchas=set();
                fDowns.close()
                ignored=[]
                downloaded=[]
                for episode in episodes:
                        try:
                                if not episode.title in gotchas:

                                        logger.debug("episodeisode: " + episode.title) 
                                        logger.debug("Downloading: " + episode.link) 

                                        tData=urllib2.urlopen(episode.link,None,10)
                                        #control gzipped data
                                        if tData.info().get('Content-Encoding') == 'gzip':
                                                logger.debug("torrent file compressed ") 
                                                buf = StringIO( tData.read())
                                                f = gzip.GzipFile(fileobj=buf)
                                                tData = f	
                                        logger.debug("Done: " + episode.link) 
                                        tFile=file(self.conf.download_dir+episode.title+".torrent",'w')
                                        tFile.write(tData.read())
                                        tFile.close()
                                        tData.close()
                                        logging.getLogger("ftorrents").debug("Downloaded "+episode.title)
                                        gotchas.add(episode.title)
                                        downloaded.append(episode)
                                else:
                                        ignored.append(episode)
                                        logging.getLogger("ftorrents").debug("Ignoring "+episode.title)

                        except Exception as e:
                                logging.getLogger("ftorrents").warning(type(e))
                                logging.getLogger("ftorrents").warning(str(e))

                fDowns=open(self.conf.cache_file,'w')
                #pickle.dump(gotchas,fDowns)
                fDowns.close()
                msg="Downloaded "+str(len(downloaded))+" torrents \n"
                logger.info(msg)
                if len(downloaded)>0:	
                        self.sendMessage(msg)

class FeedLoader:

        def __init__(self,url):
                self.url=url

        def load(self):
                d=feedparser.parse(self.url)
                return self.episodes(d.namespaces.keys()[0],d);

        def episodes(self,namespace,feed):
                eList=[]
                for entry in feed.entries:
                        e=Episode()
                        e.id=getattr(entry, namespace+'_episode')
                        e.date=entry.published
                        e.title=entry.title
                        e.link=entry.link;
                        eList.append(e)
                return eList


class Episode (object):
        def __init__(self):
                self.id=""
                self.title=""
                self.date=""
                self.link=""


        def __str__(self):
                s+="Episode id:"+self.id+"\n"
                s+="Episode:"+self.title+"\n"
                s+="Date:"+self.date+"\n"
                s+="Torrent:"+self.link+"\n"
                return s


if __name__ == "__main__":

        TorrentDowner(Config()).getTorrents()