import unittest
from mock import patch
import mock
import string
import os
import ftorrents
import yaml
import StringIO
import distutils

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
                assert conf.cache_file==os.path.join(ftorrents.config_folder(),"cache")
                assert conf.rss_url=="not_set"
                assert conf.download_dir==os.path.join(ftorrents.config_folder(),"torrent_files")
                mkpath.assert_called_once()
                dump.assert_called_once()
        

        @patch("__builtin__.open")
        def test_create_config_yaml(self,stream):
                mock.mock_open(stream);
                w=StringIO.StringIO()
                stream().write.side_effect= lambda t: w.write(t)
                ftorrents.create_config()
                cnf=yaml.load(w.getvalue())
                assert cnf.cache_file==os.path.join(ftorrents.config_folder(),"cache")
                assert cnf.rss_url=="not_set"
                assert cnf.download_dir==os.path.join(ftorrents.config_folder(),"torrent_files")

        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load_config(self,load,isfile):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=ftorrents.Config("cache","url","download")
                #get get the correct configuration
                cnf=ftorrents.load_config()
                assert cnf.cache_file=="cache"
                assert cnf.rss_url=="url"
                assert cnf.download_dir=="download"
