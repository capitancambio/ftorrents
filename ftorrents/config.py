import yaml
import os
import distutils
import logging
from distutils import dir_util
logger = logging.getLogger("ftorrents")
#Constants
CONFIG_FOLDER=".ftorrents"
CONFIG_FILE="cnf.yml"
URL_NOT_SET="http://not_set"
HISTORY_FILE="history"
TORRENTS_DIR="torrent_files"

def config_folder():
        return os.path.join(os.path.expanduser("~"),CONFIG_FOLDER)

def config_file():
        return os.path.join(config_folder(),CONFIG_FILE)

def load():
        logger.debug("Loading config")
        #check if the config folder exsists if not create it
        cnf=None
        if not os.path.isfile(config_file()):
                logger.debug("Config file not found")
                cnf=create_config()
        else:
                cnf=yaml.load(open(config_file())) 
        dir_util.mkpath(cnf.download_dir)
        logger.info("Configuration loaded %s"%cnf)
        if cnf.rss_url == URL_NOT_SET:
                raise RuntimeError("Please set the rss url in the configuration file (%s)"%config_file())

        return cnf

def create_config():
        logger.info("Creating default config file %s"%config_file())
        cnf=Config(os.path.join(config_folder(),HISTORY_FILE), URL_NOT_SET,os.path.join(config_folder(),TORRENTS_DIR))
        dir_util.mkpath(config_folder())
        with open(os.path.join(config_folder(),CONFIG_FILE),'w') as f:
                yaml.dump(cnf,f)
        return cnf

class Config:

        """configuration items"""
        def __init__(self,history_file,rss_url,download_dir):
                self.history_file   = history_file 
                self.rss_url      = rss_url
                self.download_dir = download_dir 

        def __repr__(self):
                return "Config(%r,%r,%r)" % ( self.history_file,self.rss_url,self.download_dir)
        def __str__(self):
                return "\n\thistory_file: %s\n\trss_url: %s\n\tdownload_dir: %s\n"%(self.history_file,self.rss_url,self.download_dir)
