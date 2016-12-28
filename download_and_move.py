############################################
####             IMPORTS                ####
############################################
import youtube_dl
import os
import eyed3
#TEST
import shutil
import sys

############################################
####             CLASSES                ####
############################################

class Download(object):
    '''
    This class contains functions to do with downloading the song
    and moving it. 
    '''

    def download_and_move(self, url, youtube_title, directory, playlist, song_name, artist, image_path):
        '''
        This is the top level function for downloading a song.
        In it, we download a song, append the ID3 tags, and move the song
        to the correct directory.
        '''
        self.tmp_path = os.getcwd() + '\\' + youtube_title + '-' + url + '.mp3'
        self.new_path = directory + '\\' + playlist +'\\' + song_name +'.mp3'
        self.url = url
        self.playlist = playlist
        self.song_name = song_name.encode('utf-8')
        self.artist = artist.encode('utf-8')
        self.image_path = image_path
        self.download_song()
        self.append_id3_tags()
        self.move_song()
        self.song_downloaded = True
        
    def download_song(self):
        '''
        shutil.copyfile('test.mp3', self.tmp_path)
        self.song_downloaded = True        
        This function is downloads the song video
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
                ydl.download(['http://www.youtube.com/watch?v=' + self.url])
                self.song_downloaded = True
            except:
                self.song_downloaded = False
        

        
    def append_id3_tags(self):
        '''
        The purpose of this function is to append the ID3 tags to the mp3. We append
        artist and album information, along with album art is we have it.
        '''
        mp3_file = eyed3.load(self.tmp_path)
        try:
            mp3_file.tag.title = unicode(self.song_name)
        except:
            pass
            
        try:
            mp3_file.tag.artist = unicode(self.artist)
        except:
            pass
            
        mp3_file.tag.album = unicode(self.playlist)
        image_data = open(self.image_path ,'rb').read()
        mp3_file.tag.images.set(3,image_data,'image/jpeg', u'Album art')
        '''
        Windows is annoying so we have to save the ID3 tags in some other version.
        I still can't get the pictures to work on Media Player - don't really care though         
        '''
        mp3_file.tag.save(self.tmp_path, version=(1,None,None))
        mp3_file.tag.save(self.tmp_path, version=(2,4,0))
        
 
    def move_song(self):
        '''
        The purpose of the is function is to move the mp3 file to the
        directory chosen by the user
        '''
        if not os.path.isfile(self.new_path):
            try:
                os.rename(self.tmp_path, self.new_path)
            except:
                pass
        else:
            os.remove(self.tmp_path)          

if __name__=='__main__':
    url = 'YQHsXMglC9A'
    youtube_title = 'Adele - Hello'
    directory = 'test'
    playlist = 'test_playlist'
    song_name = 'Hello'
    artist = 'Adele'
    image_path = 'album_art\\free_riddims_default.jpg'

    os.makedirs('test\\test_playlist')

    test = Download()
    test.download_and_move(url, youtube_title, directory, playlist, song_name, artist, image_path)
    file_exists = os.path.isfile('test\\test_playlist\\Hello.mp3')
    print (file_exists)

    shutil.rmtree('test')

