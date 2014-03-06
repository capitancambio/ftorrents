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

class TorrentDowner:
        def __init__(self):
                pass

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
                FILE_DOWNS='/home/javi/.ftorrent/downloads'
                RSS_URL='http://showrss.info/rss.php?user_id=116775&hd=null&proper=null&namespaces=true&magnets=false'
                DOWN_DIR="/home/javi/src/ftorrents/torrent_files/"
                #DOWN_DIR="/tmp/"
                fl=FeedLoader(RSS_URL)
                el=fl.load()
                fDowns=open(FILE_DOWNS,'r')
                gotchas=pickle.load(fDowns)
                #gotchas=set()
                fDowns.close()
                ignored=[]
                downloaded=[]
                for ep in el:
                        try:
                                if not ep.title in gotchas:

                                        logger.debug("episode: " + ep.title) 
                                        logger.debug("Downloading: " + ep.link) 
                                        tData=urllib2.urlopen(ep.link,None,10)
                                        #control gzipped data
                                        if tData.info().get('Content-Encoding') == 'gzip':
                                                logger.debug("torrent file compressed ") 
                                                buf = StringIO( tData.read())
                                                f = gzip.GzipFile(fileobj=buf)
                                                tData = f	
                                        logger.debug("Done: " + ep.link) 
                                        tFile=file(DOWN_DIR+ep.title+".torrent",'w')
                                        tFile.write(tData.read())
                                        tFile.close()
                                        tData.close()
                                        logging.getLogger("ftorrents").debug("Downloaded "+ep.title)
                                        gotchas.add(ep.title)
                                        downloaded.append(ep)
                                else:
                                        ignored.append(ep)
                                        logging.getLogger("ftorrents").debug("Ignoring "+ep.title)

                        except Exception as e:
                                logging.getLogger("ftorrents").warning(type(e))
                                logging.getLogger("ftorrents").warning(str(e))

                fDowns=open(FILE_DOWNS,'w')
                pickle.dump(gotchas,fDowns)
                fDowns.close()
                if len(downloaded)>0:	
                        msg="Downloaded "+str(len(downloaded))+" torrents \n"
                        self.sendMessage(msg)

class FeedLoader:

        def __init__(self,url):
                self.url=url

        def load(self):
                d=feedparser.parse(self.url)
                eparser=EpisodeParser(d.namespaces.keys()[0])
                elist=eparser.episodeList(d);
                return elist


class EpisodeParser:
        def __init__(self,namespace):
                self.namespace=namespace

        def episodeList(self,feed):
                eList=[]
                for entry in feed.entries:
                        e=Episode()
                        e.show_id=getattr(entry   , self.namespace+'_showid')
                        e.show_name=getattr(entry , self.namespace+'_showname')
                        e.id=getattr(entry        , self.namespace+'_episode')
                        e.date=entry.published
                        e.title=entry.title
                        e.link=entry.link;
                        eList.append(e)
                return eList


class Episode (object):
        def __init__(self):
                self.show_id=""
                self.show_name=""
                self.id=""
                self.title=""
                self.date=""
                self.link=""


        def __str__(self):
                s="Show id:"+self.show_id+"\n"
                s+="Show name:"+self.show_name+"\n"
                s+="Episode id:"+self.id+"\n"
                s+="Episode:"+self.title+"\n"
                s+="Date:"+self.date+"\n"
                s+="Torrent:"+self.link+"\n"
                return s

if __name__ == "__main__":
        TorrentDowner().getTorrents()
