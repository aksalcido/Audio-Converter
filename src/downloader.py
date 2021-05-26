from __future__ import unicode_literals
from python_settings import settings
from logger import Logger
from collections import namedtuple

import os
import youtube_dl

# Setup the GLOBAL Variables through settings.py
os.environ["SETTINGS_MODULE"] = 'settings'

# Sets up a DownloadResult namedtuple to store in Downloader history for front end display purposes
DownloadResult = namedtuple('DownloadResult', ['status', 'title', 'url'])

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
        self.running = False
        self.status = settings.WAITING_FOR_DOWNLOAD
        self.history = []

    def available(self) -> bool:
        return not self.running

    def download(self, link: str) -> None:
        """
        Args:
        link: Takes a string argument 'link' referring to the YouTube link being requested to download.

        Return:
        None, however the entirity of this program is ran through this function. The link is assigned to the
        downloader, the downloader runs and downloads the video (if valid url), and the downloader stores the
        DownloadResult in reset, and restarts to be available for the next url input.
        """
        try:
            self.assign_link(link)
            self._run()
            self.assign_status(settings.DOWNLOAD_SUCCESS)
        except (AssertionError, youtube_dl.utils.DownloadError) as e:
            self.assign_status(settings.DOWNLOAD_FAILURE)
        finally:
            print("SETTINGS?: " + str(self.status))
            self._reset()

    def _run(self) -> None:
        '''
        Runs the downloader -- asserting that there is a valid url_link and then using
        youtube-dl, downloads the requested url_link with the current settings being in
        self.ydl_opts.
        '''
        assert self.url_link
        self.running = True
        
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url_link])


    def _reset(self) -> None:
        '''
        Saves the url_link in history and then proceeds to reset the attributes of the downloader for the next download.
        '''
        self._store()
        self.assign_link(None)
        self.assign_status(settings.WAITING_FOR_DOWNLOAD)
        self.running = False

    def _store(self) -> None:
        '''
        Store a DownloadResult namedtuple for the current downloaded item. This function is called on _reset() which
        will only be invoked after a download request has been made.
        '''
        dl_res = None
        
        if self.status == settings.DOWNLOAD_SUCCESS:
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url_link)
                video_title = info_dict.get("title", None)
                dl_res = DownloadResult(settings.DOWNLOAD_SUCCESS, video_title, self.url_link)
        else:
            dl_res = DownloadResult(settings.DOWNLOAD_FAILURE, "NO TITLE", self.url_link)
        
        self.history.append(dl_res)

    def change_codec_format(self, format: str) -> None:
        '''
        Changes the codec_format in the download settings.
        Takes a format argument and assigns it in ydl_opts.
        Asserts that format must be mp3 or mp4 format.
        '''
        assert format == settings.MP3_FORMAT or format == settings.MP4_FORMAT
        self.ydl_opts['postprocessors'][0]['preferredcodec'] = format

    # Assign Functions #
    def assign_link(self, link: str) -> None:
        '''
        Set the url link for the downloader to the link argument
        '''
        self.url_link = link

    def assign_status(self, status) -> None:
        '''
        Set the status to the status argument
        '''
        self.status = status

    def assign_thread(self, thread_hook) -> None:
        '''
        Assigns the progress hook to the assigned thread. However, this function
        is not used in this current version.
        '''
        self.ydl_opts['progress_hooks'] = [thread_hook]

    # Get Function #
    def get_history(self) -> [DownloadResult]:
        '''
        Returns the list of DownloadResults for the current session.
        '''
        return self.history

    def _hook(self, d) -> None:
        '''
        Download message kept in ydl_opts to see completion of download.
        '''
        if d['status'] == 'finished':
            print('Done downloading, now converting...')

if __name__ == '__main__':
    downloader = Downloader()
    downloader.download("https://www.youtube.com/watch?v=umjPSpcqL9w")
    downloader.download("https://www.youtube.com/watch?v=ZEcqHA7dbwM")