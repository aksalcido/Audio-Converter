from __future__ import unicode_literals

class Logger(object):
    '''
    Creates a logger object for our Downloader Class. Taken from the youtube-dl
    Logger class template and essentially prints messages for developer purposes.
    '''
    def debug(self, msg):
        print(msg)
    
    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)