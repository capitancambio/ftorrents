ftorrents
=========

ftorrents is a small program that fetches the latest torrent files from (showsrss.info)[http://showsrss.info]. To configure it just run it one time to generate the configuration file, then edit the file adding the rss url. Make sure that you have generated the url including namespaces and disallowing magnet links. 

The downloaded files will be stored in ```~/.ftorrents/torrent_files```, or in the folder indicated in the configuration file.
