from download_thread import DownloadThread
from flask import Flask, render_template, request, url_for
from python_settings import settings
from downloader import Downloader
from download_thread import DownloadThread

app = Flask(__name__)
downloader = Downloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_link = request.form.get('url')
        download_thread = DownloadThread(downloader)
        
        if downloader.download(url_link) == settings.DOWNLOAD_SUCCESS:
            return render_template('index.html')
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')

# Running on http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True)
    print("Hello world!")



# Links
# https://www.youtube.com/watch?v=umjPSpcqL9w               -- Valid
# https://www.youtube.com/watch?v=ZEcqHA7dbwM               -- Valid
# https://www.youtube.com/watch?v=ZEcasdadasdsadsaqHA7dbwM  -- Invalid