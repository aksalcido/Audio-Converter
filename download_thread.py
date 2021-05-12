import threading
import time

class DownloadThread(threading.Thread):
    def __init__(self, downloader):
        self.progress = 0
        self.downloader = downloader
        super().__init__()
    
    def run(self, url_link):
        self.downloader.assign_thread(self.hook)

        if self..download(url_link) == settings.DOWNLOAD_SUCCESS:
            pass

    def hook(self, d):
        if d['status'] == 'downloading':
            self.progress = d['_percent_str']