import youtube_dl
import os
import eyed3

class Download(object):

    def download_song(self, url):
        '''
        This function downloads the audio of a youtube video
        :param url: The specific id of the youtube url
        '''
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }]
            }

        with youtube_dl.YoutubeDL(options) as ydl:
            try:
                ydl.download(['http://www.youtube.com/watch?v=' + url])
                song_downloaded = True
            except:
                song_downloaded = False
        return song_downloaded
