from download_thread import DownloadThread
from flask import Flask, render_template, request, redirect, url_for
from python_settings import settings
from downloader import Downloader

app = Flask(__name__, static_folder="../static", template_folder="../templates")
downloader = Downloader()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('/index.html', downloader=downloader, history=downloader.get_history())

@app.route('/convert', methods=['POST'])
def convert():
    url_link = request.form.get('url')

    if downloader.available():
        downloader.download(url_link)

    return redirect('/')

@app.route('/change_format', methods=['POST'])
def change_format():
    print("change: ? ")

    if request.method == "POST":
        if request.form['format-button'] == 'MP3' or request.form['format-button'] == 'MP4':
            downloader.change_codec_format(request.form['format-button'].lower())

    return redirect('/')

# Running on http://127.0.0.1:5000/
if __name__ == '__main__':
    app.run(debug=False, threaded=True)

# https://www.youtube.com/watch?v=JQFeEscCvTg