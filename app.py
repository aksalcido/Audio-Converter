from download_thread import DownloadThread
from flask import Flask, render_template, request, redirect, url_for
from python_settings import settings
from downloader import Downloader

app = Flask(__name__)
downloader = Downloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_link = request.form.get('url')
        download_result = downloader.download(url_link)
        return render_template('index.html', history=downloader.get_history())
    else:
        return render_template('index.html')

@app.route('/<url>')
def download_index(url):
    
    
    return render_template('index.html')

# Running on http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    print("Hello world!")

# Links
# https://www.youtube.com/watch?v=umjPSpcqL9w               -- Valid
# https://www.youtube.com/watch?v=ZEcqHA7dbwM               -- Valid
# https://www.youtube.com/watch?v=ZEcasdadasdsadsaqHA7dbwM  -- Invalid