import unittest
from mock import patch
import mock
import string
import os
import config 
import yaml
import StringIO
import distutils
import logging
#avoid logs during unittesting
logging.disable(logging.CRITICAL)

class ConfigTests(unittest.TestCase):
        @patch('os.path.expanduser')
        def test_check_config_folder(self,home):
                #check that the config_folder returns the appropriate value
                home.return_value="/home/user"
                assert config.config_folder()=="/home/user/%s"%config.CONFIG_FOLDER

        def test_check_config_file(self):
                #check that the config_file returns the appropriate value
                assert config.config_file()==os.path.join(config.config_folder(),"cnf.yml")

        @patch('distutils.dir_util.mkpath')
        @patch('os.path.isfile')
        @patch('ftorrents.config.create_config')
        def test_load_calls_create(self,create_config,isfile,mkpath):
                #if the config folder doesn't exsists
                isfile.return_value=False
                #and we try to load the configuration
                config.load()
                #we try to create the configuration 
                create_config.assert_called_once_with()
                

        @patch('distutils.dir_util.mkpath')
        @patch("yaml.dump")
        @patch("__builtin__.open")
        def test_create_config(self,stream,dump,mkpath):
                conf=config.create_config()
                assert conf.history_file==os.path.join(config.config_folder(),config.HISTORY_FILE)
                assert conf.rss_url==config.URL_NOT_SET
                assert conf.download_dir==os.path.join(config.config_folder(),config.TORRENTS_DIR)
                mkpath.assert_called_once()
                dump.assert_called_once()
        

        @patch("__builtin__.open")
        def test_create_config_yaml(self,stream):
                mock.mock_open(stream);
                w=StringIO.StringIO()
                stream().write.side_effect= lambda t: w.write(t)
                config.create_config()
                cnf=yaml.load(w.getvalue())
                assert cnf.history_file==os.path.join(config.config_folder(),config.HISTORY_FILE)
                assert cnf.rss_url==config.URL_NOT_SET
                assert cnf.download_dir==os.path.join(config.config_folder(),config.TORRENTS_DIR)

        @patch("__builtin__.open")
        def test_create_config_yaml(self,stream):
                mock.mock_open(stream);
                w=StringIO.StringIO()
                stream().write.side_effect= lambda t: w.write(t)
                config.create_config()
                cnf=yaml.load(w.getvalue())
                assert cnf.history_file==os.path.join(config.config_folder(),config.HISTORY_FILE)
                assert cnf.rss_url==config.URL_NOT_SET
                assert cnf.download_dir==os.path.join(config.config_folder(),config.TORRENTS_DIR)

        @patch('distutils.dir_util.mkpath')
        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load_url_not_set(self,load,isfile,mkpath):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=config.Config("history",config.URL_NOT_SET,"download")
                #get the correct configuration and fail because the url is not set
                try:
                        cnf=config.load()
                        self.fail("Exception wasn't thrown")
                except:
                        pass

        @patch("__builtin__.open")
        @patch('distutils.dir_util.mkpath')
        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load(self,load,isfile,mkpath,open):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=config.Config("history","url","download")
                #get get the correct configuration
                cnf=config.load()
                assert cnf.history_file=="history"
                assert cnf.rss_url=="url"
                assert cnf.download_dir=="download"

        @patch("__builtin__.open")
        @patch('distutils.dir_util.mkpath')
        @patch('os.path.isfile')
        @patch('yaml.load')
        def test_load_config_creates_download_folder(self,load,isfile,mkpath,open):
                #if the config file exists 
                isfile.return_value=True
                #and the contents from yaml are these
                load.return_value=config.Config("history","url","download")
                #get get the correct configuration
                cnf=config.load()
                mkpath.assert_called_once_with("download")
