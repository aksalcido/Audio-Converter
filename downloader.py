from __future__ import unicode_literals
from python_settings import settings
from logger import Logger
import os
import youtube_dl

# Setup the GLOBAL Variables through settings.py
os.environ["SETTINGS_MODULE"] = 'settings'

# https://stackoverflow.com/questions/13034496/using-global-variables-between-files
class Downloader:

    def __init__(self):
        '''
        Initializes a Downloader object that keeps the current settings required for youtube-dl.
        Stores a single link (could possibly be implemented as a list of links for batch downloading),
        because an individual link does what we need to accomplish and because Users should not be able 
        to spam urls (too many requests).
        '''
        self.ydl_opts = {
            'outtmpl': '/downloads/%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': settings.MP3_FORMAT,
                'preferredquality': '192',
            }],
            'logger': Logger(),
            'progress_hooks': [self._hook],
            'nooverwrites': True,
            'noplaylist': True
        }
        self.url_link = None
        self.status = settings.WAITING_FOR_DOWNLOAD
        self.history = []

    def download(self, link) -> int:
        '''
        Takes a valid url link argument and assigns it to the Downloaders self.url_link attribute.
        Then runs the downloader and downloads the url argument leading to a download_result.
        Stores the download_result, resets the downloader and returns the result to user.
        '''
        self.assign_link(link)
        self._run()
        download_result = self.status
        self._reset()

        return download_result

    def _run(self):
        '''
        Runs the downloader -- asserting that there is a valid url_link and then using
        youtube-dl, downloads the requested url_link with the current settings being in
        self.ydl_opts.
        '''
        try:
            assert self.url_link

            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([self.url_link])
    
        except (AssertionError, youtube_dl.utils.DownloadError) as e:
            self.assign_status(settings.DOWNLOAD_FAILURE)
        else:
            self.assign_status(settings.DOWNLOAD_SUCCESS)
    
    def assign_link(self, link: str):
        '''
        Set the url link for the downloader to the link argument
        '''
        self.url_link = link

    def assign_status(self, status):
        '''
        Set the status to the status argument
        '''
        self.status = status

    def assign_thread(self, thread_hook):
        self.ydl_opts['progress_hooks'] = [thread_hook]

    def get_history(self) -> list:
        return self.history
    
    def change_codec_format(self, format: str):
        '''
        Changes the codec_format in the download settings.
        Takes a format argument and assigns it in ydl_opts.
        Asserts that format must be mp3 or mp4 format.
        '''
        assert format == settings.MP3_FORMAT or format == settings.MP4_FORMAT
        self.ydl_opts['postprocessors'][0]['preferredcodec'] = format

    def _reset(self):
        '''
        Saves the url_link in history and then proceeds to reset the attributes of the downloader for the next download.
        '''
        self.history.append(self.url_link)
        self.assign_link(None)
        self.assign_status(settings.WAITING_FOR_DOWNLOAD)

    def _hook(self, d):
        '''
        Download message kept in ydl_opts to see completion of download.
        '''
        if d['status'] == 'finished':
            print('Done downloading, now converting...')

'''
if __name__ == '__main__':
    downloader = Downloader()

    downloader.download("https://www.youtube.com/watch?v=umjPSpcqL9w")
    downloader.download("https://www.youtube.com/watch?v=ZEcqHA7dbwM")
'''