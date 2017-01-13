from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
import mutagen
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

    def append_tags(self, mp3_file, song, artist, playlist, album_art):
        '''
        Appends ID3 tags to the mp3 file.
        :param filename: The mp3 we plan to append tags to
        :param song: The name of the song.
        :param artist: The name of the artist
        :param album_art: A file path to the album art.
        '''
        mp3 = eyed3.load(mp3_file)
        mp3.tag.title = unicode(song)
        mp3.tag.artist = unicode(artist)
        mp3.tag.album = unicode(playlist)
        image_data = open(album_art, 'rb').read()
        mp3.tag.images.set(3, image_data, 'image/jpeg', u'Album art')
        '''
        Windows is annoying so we have to save the ID3 tags in some other version.
        I still can't get the pictures to work on Media Player - don't really care though
        '''
        #mp3_file.tag.save(mp3, version=(1, None, None))
        mp3.tag.save(mp3, version=(2, 4, 0))

    def move_song(self, orig_filepath, new_filepath):
        '''
        As a result of youtube_dl being a bit shit, we have to move the song
        :return:
        '''
        os.rename(orig_filepath, new_filepath)

    ############################################

    def append_tags_3(self, mp3_path, song, artist, playlist, album_art):
        '''
        Appends ID3 tags to the mp3 file.
        :param filename: The mp3 we plan to append tags to
        :param song: The name of the song.
        :param artist: The name of the artist
        :param album_art: A file path to the album art.
        '''

        audio = ID3('music_test\\test.mp3')
        audio["TIT2"] = TIT2(encoding=2, text='blha')
        audio["TPE1"] = TPE1(encoding=2, text=' Artist')
        audio["TALB"] = TALB(encoding=2, text='mutagen Album Name')
        audio.save(v2_version=3)

        audio = MP3('music_test\\test.mp3', ID3=ID3)
        audio.add_tags()

        audio.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/png',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=open('album_art\\free_riddims_default.jpg').read()
            )
        )
        audio.save(v2_version=3)


    def append_tags_2(self, mp3_path, song, artist, playlist, album_art):
        '''
        Appends ID3 tags to the mp3 file.
        :param filename: The mp3 we plan to append tags to
        :param song: The name of the song.
        :param artist: The name of the artist
        :param album_art: A file path to the album art.
        '''

        try:
            mp3 = EasyID3(mp3_path)
        except:
            mp3 = mutagen.File(mp3_path, easy=True)
            mp3.add_tags()

        mp3['title'] = song
        mp3['artist'] = artist
        mp3['album'] = playlist
        mp3.save(v2_version=3)
        mp3.tags.add(
            APIC(
                encoding=3,  # 3 is for utf-8
                mime='image/jpeg',  # image/jpeg or image/png
                type=3,  # 3 is for the cover image
                desc=u'Cover',
                data=open(album_art).read()
            )
        )
