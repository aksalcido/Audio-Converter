import threading
import time
from python_settings import settings

class DownloadThread(threading.Thread):
    '''
    Not currently used in this project.
    '''
    def __init__(self, downloader):
        self.progress = 0
        self.downloader = downloader
        super().__init__()

    def run(self):
        self.downloader.assign_thread(self.hook)

        if self.downloader.download() == settings.DOWNLOAD_SUCCESS:
            pass
        else:
            for _ in range(10):
                time.sleep(1)
                self.progress += 10
                print(self.progress)

    def get_progress(self):
        return self.progress

    def hook(self, d):
        if d['status'] == 'downloading':
            self.progress = d['_percent_str']
            print("Progress: ", self.progress)