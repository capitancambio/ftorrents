import unittest
from mock import patch
import mock
import string
import os
import ftorrents
import yaml
import StringIO
import distutils
import urllib2
import logging
#avoid logs during unittesting
logging.disable(logging.CRITICAL)

RSS_EXAMPLE=""" 
<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:showrss="http://showrss.info/" version="2.0">
  <channel>
    <title>showRSS: feed for Game of Thrones</title>
    <link>http://showrss.info/?cs=browse&amp;show=350</link>
    <ttl>30</ttl>
    <description>showRSS feed Game of Thrones</description>
    <item>
      <title>Game of Thrones 4x02 The Lion and the Rose 720p</title>
      <link>magnet:?xt=urn:btih:BCE21308AFAB5BD10AECA40C8F9861708B5309E1&amp;dn=Game+of+Thrones+S04E02+720p+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce</link>
      <guid isPermaLink="false">568316b13c072fc9d660f72759920163</guid>
      <pubDate>Mon, 14 Apr 2014 03:30:01 +0000</pubDate>
      <description>New HD 720p torrent: Game of Thrones 4x02 The Lion and the Rose 720p. Link: &lt;a href="magnet:?xt=urn:btih:BCE21308AFAB5BD10AECA40C8F9861708B5309E1&amp;dn=Game+of+Thrones+S04E02+720p+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce"&gt;magnet:?xt=urn:btih:BCE21308AFAB5BD10AECA40C8F9861708B5309E1&amp;dn=Game+of+Thrones+S04E02+720p+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce&lt;/a&gt;</description>
      <showrss:showid>350</showrss:showid>
      <showrss:showname>Game of Thrones</showrss:showname>
      <showrss:episode>36710</showrss:episode>
      <showrss:info_hash>BCE21308AFAB5BD10AECA40C8F9861708B5309E1</showrss:info_hash>
      <showrss:rawtitle>Game of Thrones S04E02 720p HDTV x264 2HD</showrss:rawtitle>
      <enclosure url="magnet:?xt=urn:btih:BCE21308AFAB5BD10AECA40C8F9861708B5309E1&amp;dn=Game+of+Thrones+S04E02+720p+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce" length="0" type="application/x-bittorrent"/>
    </item>
    <item>
      <title>Game of Thrones 4x02 The Lion and the Rose</title>
      <link>magnet:?xt=urn:btih:BED425AD8C96FF8645E4674762DC86C3CD123CDE&amp;dn=Game+of+Thrones+S04E02+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce</link>
      <guid isPermaLink="false">d7d5b9548c2e0513a2b2883aa47513b1</guid>
      <pubDate>Mon, 14 Apr 2014 02:30:01 +0000</pubDate>
      <description>New standard torrent: Game of Thrones 4x02 The Lion and the Rose. Link: &lt;a href="magnet:?xt=urn:btih:BED425AD8C96FF8645E4674762DC86C3CD123CDE&amp;dn=Game+of+Thrones+S04E02+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce"&gt;magnet:?xt=urn:btih:BED425AD8C96FF8645E4674762DC86C3CD123CDE&amp;dn=Game+of+Thrones+S04E02+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce&lt;/a&gt;</description>
      <showrss:showid>350</showrss:showid>
      <showrss:showname>Game of Thrones</showrss:showname>
      <showrss:episode>36701</showrss:episode>
      <showrss:info_hash>BED425AD8C96FF8645E4674762DC86C3CD123CDE</showrss:info_hash>
      <showrss:rawtitle>Game of Thrones S04E02 HDTV x264 2HD</showrss:rawtitle>
      <enclosure url="magnet:?xt=urn:btih:BED425AD8C96FF8645E4674762DC86C3CD123CDE&amp;dn=Game+of+Thrones+S04E02+HDTV+x264+2HD&amp;tr=udp://tracker.openbittorrent.com:80&amp;tr=udp://tracker.publicbt.com:80&amp;tr=udp://tracker.istole.it:80&amp;tr=http://tracker.istole.it&amp;tr=http://fr33dom.h33t.com:3310/announce" length="0" type="application/x-bittorrent"/>
    </item>
  </channel>
</rss>
"""

class FtorrentsTests(unittest.TestCase):


        @patch('os.path.expanduser')
        def test_check_config_folder(self,home):
                #check that the config_folder returns the appropriate value
                home.return_value="/home/user"
                assert ftorrents.config_folder()=="/home/user/%s"%ftorrents.CONFIG_FOLDER

        def test_check_config_file(self):
                #check that the config_file returns the appropriate value
                assert ftorrents.config_file()==os.path.join(ftorrents.config_folder(),"cnf.yml")

        @patch('os.path.isfile')
        @patch('ftorrents.create_config')
        def test_load_calls_create(self,create_config,isfile):
                #if the config folder doesn't exsists
                isfile.return_value=False
                #and we try to load the configuration
                ftorrents.load_config()
                #we try to create the configuration 
                create_config.assert_called_once_with()
                

        @patch('distutils.dir_util.mkpath')
        @patch("yaml.dump")
        @patch("__builtin__.open")
        def test_create_config(self,stream,dump,mkpath):
                conf=ftorrents.create_config()
                assert conf.history_file==os.path.join(ftorrents.config_folder(),ftorrents.HISTORY_FILE)
                assert conf.rss_url==ftorrents.URL_NOT_SET
                assert conf.download_dir==os.path.join(ftorrents.config_folder(),ftorrents.TORRENTS_DIR)
                mkpath.assert_called_once()
                dump.assert_called_once()
        

        @patch("__builtin__.open")
        def test_create_config_yaml(self,stream):
                mock.mock_open(stream);
                w=StringIO.StringIO()
                stream().write.side_effect= lambda t: w.write(t)
                ftorrents.create_config()
                cnf=yaml.load(w.getvalue())
                assert cnf.history_file==os.path.join(ftorrents.config_folder(),ftorrents.HISTORY_FILE)
                assert cnf.rss_url=="not_set"
                assert cnf.download_dir==os.path.join(ftorrents.config_folder(),ftorrents.TORRENTS_DIR)

        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load_url_not_set(self,load,isfile):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=ftorrents.Config("history",ftorrents.URL_NOT_SET,"download")
                #get the correct configuration and fail because the url is not set
                try:
                        cnf=ftorrents.load_config()
                        self.fail("Exception wasn't thrown")
                except:
                        pass

        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load_config(self,load,isfile):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=ftorrents.Config("history","url","download")
                #get get the correct configuration
                cnf=ftorrents.load_config()
                assert cnf.history_file=="history"
                assert cnf.rss_url=="url"
                assert cnf.download_dir=="download"

        
        def test_load_episodes(self): 
                episodes=ftorrents.FeedLoader(RSS_EXAMPLE).load()
                self.assertEquals(2,len(episodes),"We got two episodes")
                self.assertEquals("Game of Thrones 4x02 The Lion and the Rose 720p",episodes[0].title)


        @patch('os.path.isfile')
        def test_load_history_empty(self,isfile):
                isfile.return_value=False
                cnf=ftorrents.Config("a","a","a")
                history=ftorrents.TorrentDownloader(cnf).getHistory()
                self.assertEqual(0,len(history),"The new history is empty")

        @patch('os.path.isfile')
        @patch('pickle.load')
        def test_load_history(self,pload,isfile):
                #fix context 
                r=ftorrents.FeedLoader(RSS_EXAMPLE).load()
                isfile.return_value=True
                pload.return_value=ftorrents.FeedLoader(RSS_EXAMPLE).load()
                with patch("__builtin__.open") as stream:
                        cnf=ftorrents.Config("a","a","a")
                        #get the pickled history
                        history=ftorrents.TorrentDownloader(cnf).getHistory()
                        #check that is correct
                        self.assertEqual(2,len(history),"The history has been read correctly")

        @patch('pickle.dump')
        def test_save_history(self,pickle):
                #fix context 
                history=(1,2,3)
                result=[]
                pickle.side_effect=lambda c,f: result.append(c) 
                with patch("__builtin__.open") as stream:
                        cnf=ftorrents.Config("a","a","a")
                        #get the pickled history
                        ftorrents.TorrentDownloader(cnf).dumpHistory(history)
                        #check that is correct
                        self.assertEqual(result[0],history,"The history has been dumped correctly")


        @patch("urllib2.urlopen")
        def test_torrent_link_not_compressed(self,urlconnection):
                #The connection is not gzipped
                urlconnection.info().get.return_value='xml'
                #open the torrent link
                with ftorrents.TorrentLink("url!") as link:
                        #and read the contents
                        data=link.read()
                #the data has been read
                urlconnection.read.assert_called_once()
                #and the link closed
                urlconnection.closed.assert_called_once()

        @patch("gzip.GzipFile")
        @patch("urllib2.urlopen")
        def test_torrent_link_compressed(self,urlconnection,zipFile):
                #The connection is not gzipped
                urlconnection().info().get.return_value='gzip'
                #open the torrent link
                with ftorrents.TorrentLink("url!") as link:
                        #and read the contents
                        data=link.read()
                #the data has been unzipped and read 
                zipFile.read.assert_called_once()
                #and the link closed
                urlconnection.closed.assert_called_once()

        @patch("ftorrents.TorrentLink")
        @patch("__builtin__.open")
        def test_download_episode_ok(self,stream,link):
                ep=ftorrents.Episode()
                ep.title="title"
                ep.link="link"
                cnf=ftorrents.Config("a","a","a")
                self.assertTrue(ftorrents.TorrentDownloader(cnf).downloadEpisode(ep),"We got the epsisode")
                stream().write.assert_called_once()
                link.read.assert_called_once()

        @patch("ftorrents.TorrentLink")
        @patch("__builtin__.open")
        def test_download_episode_error(self,stream,link):
                def err():
                        raise Exception()
                ep=ftorrents.Episode()
                ep.title="title"
                ep.link="link"
                link().__enter__().read.side_effect=err
                cnf=ftorrents.Config("a","a","a")
                self.assertFalse(ftorrents.TorrentDownloader(cnf).downloadEpisode(ep),"We didn't got the epsisode")

        def test_get_torrents_all(self):
                #simple config
                cnf=ftorrents.Config("a",RSS_EXAMPLE,"a")
                downer=ftorrents.TorrentDownloader(cnf)
                #emtpy history
                downer.getHistory=mock.Mock(return_value=set())
                downer.dumpHistory=mock.Mock()
                downer.downloadEpisode=mock.Mock(return_value=True)
                #we expect to download all the torrents in the rss example
                eps=downer.download()
                self.assertEqual(2,len(eps),"we got two torrents!")

        def test_get_torrents_ignore_history(self):
                #simple config
                cnf=ftorrents.Config("a",RSS_EXAMPLE,"a")
                episodes=ftorrents.FeedLoader(RSS_EXAMPLE).load()
                downer=ftorrents.TorrentDownloader(cnf)
                #history already has the episodes
                downer.getHistory=mock.Mock(return_value=set([ e.title for e in episodes]))
                downer.dumpHistory=mock.Mock()
                downer.downloadEpisode=mock.Mock(return_value=True)
                #we expect to get an empty list
                eps=downer.download()
                self.assertEqual(0,len(eps),"all the torrents were ignored")
