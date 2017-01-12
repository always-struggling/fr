import youtube_dl
import os
import eyed3

class Download(object):

    def __init__(self):
        self.music_dir = 'C:\\Users\\User\\Documents\\python\\projects\\fr\\music_test\\'

    def get_song(self, url, title, song, artist, playlist, album_art):
        '''
        Top level function for downloading a song, appending ID3 tags,
        and moving it into the correct directory
        :return:
        '''
        song_downloaded = self.download_song(url)
        if song_downloaded:
            tmp_filename = os.getcwd() + '\\' + title + '-' + url + '.mp3'
            self.append_tags(tmp_filename, song, artist, playlist, album_art)
            self.move_song(tmp_filename, self.music_dir + song + '.mp3')


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

    def append_tags(self, mp3, song, artist, playlist, album_art):
        '''
        Appends ID3 tags to the mp3 file.
        :param filename: The mp3 we plan to append tags to
        :param song: The name of the song.
        :param artist: The name of the artist
        :param album_art: A file path to the album art.
        '''
        mp3_file = eyed3.load(mp3)
        mp3_file.tag.title = unicode(song)
        mp3_file.tag.artist = unicode(artist)
        mp3_file.tag.album = unicode(playlist)
        image_data = open(album_art, 'rb').read()
        mp3_file.tag.images.set(3, image_data, 'image/jpeg', u'Album art')
        '''
        Windows is annoying so we have to save the ID3 tags in some other version.
        I still can't get the pictures to work on Media Player - don't really care though
        '''
        #mp3_file.tag.save(mp3, version=(1, None, None))
        mp3_file.tag.save(mp3, version=(2, 4, 0))

    def move_song(self, orig_filepath, new_filepath):
        '''
        As a result of youtube_dl being a bit shit, we have to move the song
        :return:
        '''
        os.rename(orig_filepath, new_filepath)

