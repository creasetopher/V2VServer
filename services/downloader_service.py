# importing the module
from pytube import YouTube
import moviepy.editor as mp
from os import remove

# where to save

SAVE_PATH = "./resources/downloads/"  # to_do
class DownloadService:
    def __init__(self):

        # a YouTube object, check pytube docs
        self.media = None

    # if successful, sets media to YouTube obj and returns true
    def fetch(self, url) -> bool:
        try:
            yt = YouTube(url)
            self.media = yt
            return True
        except Exception as e:
            return False

    # def get_info(self, url):
    #     try:
    #         yt = YouTube(url)
    #         return yt.title
    #     except Exception as e:
    #         print("exception below")
    #         print(str(e))  # to handle exception
    #         return None


    def get_audio(self):
        streams = self.media.streams
        if streams:
            stream = streams.first()
            filename = self.media.title
            filename = filename.replace('/', '-')

            # download mp4 from youtube
            dl_path = stream.download(filename = filename)

            # convert mp4 to mp3
            clip = mp.AudioFileClip(dl_path)

            output_filepath = SAVE_PATH + filename + '.mp3'

            # write mp3 to resources dir
            clip.write_audiofile(output_filepath)

            print("Deleting audio file from " + dl_path)
            remove(dl_path)
            return output_filepath


    def get_info(self):
        if self.media:
            return {
                "success": True,
                "track": {
                    "title": self.media.title,
                    "description": self.media.description,
                    "author": self.media.author,
                    "views": self.media.views,
                    "length": self.media.length,
                    "rating": self.media.rating,
                    "thumbnail": self.media.thumbnail_url
                }
            }

        else:
            return {
                "success": False,
                "track": {}
            }

# d = DownloadService()
# d.get_audio(d.fetch('https://www.youtube.com/watch?v=5Eq1VgHuk9A').streams)
# d.fetch('https://www.youtube.com/watch?v=5Eq1VgHuk9A')
# d.get_audio()


