from flask import Flask, request, send_file, after_this_request, jsonify
from services.downloader_service import DownloadService
from os import remove
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify(message="hi")

service = DownloadService()
VALID_SYMBOLS = "!@#$%^&*()_-+={}[]"
DIR_DELIMITER = "/"

@app.route('/api/utils/v2v/validate')
def validate():
    url = request.args.get('url')
    service.fetch(url)
    return service.get_info()


@app.route('/api/utils/v2v/download')
def download():
    # if user hits dl again, ensure it sends vid url in request to get stream again
    # if not service.media:

    download_path = service.get_audio()
    filename = service.media.title
    sanitized_filename = ""
    for char in filename:
        if not char.isalnum() and char not in VALID_SYMBOLS:
            if char == DIR_DELIMITER:
                sanitized_filename += "-"
        else:
            sanitized_filename += char

    # filename = filename.replace('/', '-')

    @after_this_request
    def cleanup(response):
        print("Deleting audio file")
        remove(download_path)
        return response

    return send_file(download_path,
                     attachment_filename = sanitized_filename + '.mp3')
