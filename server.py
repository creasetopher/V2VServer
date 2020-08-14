from flask import Flask, request, send_file
from services.downloader_service import DownloadService
app = Flask(__name__)

service = DownloadService()

@app.route('/api/utils/v2v/validate')
def validate():
    url = request.args.get('url')
    service.fetch(url)
    return service.get_info()



@app.route('/api/utils/v2v/download')
def download():
    downloadPath = service.get_audio()
    filename = service.media.title
    filename = filename.replace('/', '-')
    return send_file(downloadPath,
                     attachment_filename= filename + '.mp3')
