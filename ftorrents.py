#!/usr/bin/python
import urllib2
from StringIO import StringIO
import gzip
import pickle
import pynotify
import feedparser
import distutils
import gtk
import os

import logging
import yaml
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

CONFIG_FOLDER=".ftorrents"

def config_folder():
        return os.path.join(os.path.expanduser("~"),CONFIG_FOLDER)

def config_file():
        return os.path.join(config_folder(),"cnf.yml")

def load_config():
        logger.debug("Loading config")
        #check if the config folder exsists if not create it
        cnf=None
        if not os.path.isfile(config_file()):
                logger.debug("Config file not found")
                cnf=create_config()
        else:
                cnf=yaml.load(config_file()) 
        logger.info("Configuration loaded %s"%cnf)
        return cnf

def create_config():
        logger.info("Creating default config file %s"%config_file())
        cnf=Config(os.path.join(config_folder(),"cache"), "not_set",os.path.join(config_folder(),"torrent_files"))
        distutils.dir_util.mkpath(config_folder())
        with open(os.path.join(config_folder(),"cnf.yml")) as f:
                yaml.dump(cnf,f)
        return cnf

class Config:

        """configuration items"""
        def __init__(self,cache_file,rss_url,download_dir):
                self.cache_file   = cache_file 
                self.rss_url      = rss_url
                self.download_dir = download_dir 

        def __repr__(self):
                return "%s(%s,%s,%s)" % (self.__class__, self.cache_file,self.rss_url,self.download_dir)
                


class TorrentDowner:
        def __init__(self,conf):
                self.conf=conf

        #def openTransmission(self,n,action):
                #assert action == "default"
                #try:
                        #os.popen2("transmission-gtk")
                        #logging.getLogger("ftorrents").debug("Transmision open!")	
                #except Exception as err:
                        #logging.getLogger("ftorrents").warning(err)

                #n.close()
                #gtk.main_quit()

        #def closeLoop(self,n):
                #print "close loop..."
                #logging.getLogger("ftorrents").debug("closing without openining transmission")	
                #n.close()
                #gtk.main_quit()


        #def sendMessage(self,msg):
                #pynotify.init("Ftorrents")
                #notice = pynotify.Notification("Ftorrents", msg)
                #notice.add_action("default", "Open Transmission", self.openTransmission)
                #notice.connect("closed",self.closeLoop)
                #notice.set_urgency(pynotify.URGENCY_LOW)
                #try:
                        #notice.show()
                        #gtk.main()

                #except Exception as err:
                        #logging.getLogger("ftorrents").warning(err)	
                #pass


        def getCache(self):
                cache=set();
                if os.path.isfile(self.conf.cache_file):
                        with open(self.conf.cache_file,'r') as f:
                                cache=pickle.load(f)
                else:
                        logger.warning("Couldn't load the cache file")

                return cache

        def dumpCache(self,cache):
                with open(self.conf.cache_file) as f:
                        pickle.dump(cache,f)

        def downloadEpisode(self,episode):
                try:
                        #control gzipped data
                        with open(self.conf.download_dir+episode.title+".torrent",'w') as tFile:
                                with TorrentLink(episode.link) as tData:
                                        #write the data
                                        tFile.write(tData.read())
                                        logging.getLogger("ftorrents").debug("Downloaded "+episode.title)
                        return True
                except Exception as e:
                        logging.getLogger("ftorrents").warning(type(e))
                        logging.getLogger("ftorrents").warning(str(e))
                        return False

        
        def getTorrents(self):
                logging.getLogger("ftorrents").debug("Starting to download torrents")
                #get the feeds
                episodes=FeedLoader(self.conf.rss_url).load()
                #load cache
                cache=self.getCache()
                downloaded=[] 
                for episode in episodes :
                        #not in the history 
                        if  not episode.title in cache:
                                #has been downloaded properly
                                if self.downloadEpisode(episode):
                                        cache.add(episode.title)
                                        downloaded.append(episode)
                        else:
                                logging.getLogger("ftorrents").debug("Ignoring "+episode.title)

                self.dumpCache(cache)
                msg="Downloaded "+str(len(downloaded))+" torrents \n"
                logger.info(msg)
                return downloaded

class TorrentLink(object):
        """docstring for TorrentLink"""
        def __init__(self, url):
                self.url = url
                self.closeable=None
                self.doRead=None

        
        def __enter__(self):
                """ Gets the url and reads the data making sure that
                if process it if it's gzipped"""
                #get link by opening the link
                urlData=urllib2.urlopen(self.url,None,10)
                #if is compressed prepare the data
                #control gzipped data
                if urlData.info().get('Content-Encoding') == 'gzip':
                        logger.debug("torrent file compressed ") 
                        self.doRead=lambda :gzip.GzipFile(StringIO(urlData.read())).read()
                else:
                        self.doRead=lambda : urlData.read()
                self.closeable=urlData
                return self

        def read(self):
                return self.doRead()

        def __exit__(self,type, value, traceback):
                self.closeable.close()
                

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
                s="Episode id:"+self.id+"\n"
                s+="Episode:"+self.title+"\n"
                s+="Date:"+self.date+"\n"
                s+="Torrent:"+self.link+"\n"
                return s


if __name__ == "__main__":

        TorrentDowner(Config()).getTorrents()
