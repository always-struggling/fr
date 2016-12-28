############################################
####             IMPORTS                ####
############################################
from music_db import MusicDB
from bs4 import BeautifulSoup
from PIL import Image
import urllib as dwn
import requests


db = MusicDB()
############################################
####             CLASSES                ####
############################################

class Art(object):

    '''
    This class contains the functions for retrieving
    album art for an artist
    '''

    def __init__(self):

        self.default_image = 'album_art\\free_riddims_default.jpg'
        self.all_art = dict(db.get_all_art())


    def get_album_art(self, artist):
        '''
        This function is the top level function for retrieving
        album art for an artist. It takes an artist as a parameter
        and searches the database for the image path of an existing
        image If none exists, it then attempts to scrape one from the
        internet. If we are still unable to find one it returns the default
        free riddims album art.
        '''
        self.artist = artist
        try:
            self.image_path = self.all_art[self.artist]
        except:
            self.image_path = None

        if self.image_path is None:
            self.download_art()
            if self.image_path is None:
                self.image_path = self.default_image
        return self.image_path


    def download_art(self):
        '''
        This function attempts to scrape an album cover from
        the website www.covermytumes.
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = 'http://www.covermytunes.com/search.php?search_query=' + self.artist.replace(' ', '+') +'&x=0&y=0'
        html = requests.get(url, headers = headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        if len(soup.find_all('h2')) == 0:
            image_urls = soup.find_all('img')
            image_urls = [(e.get('src'), e.get('height'), e.get('width')) for e in image_urls ]
            self.image_path = 'album_art\\' + self.artist + '.jpg'
            dwn.urlretrieve(image_urls[0][0], self.image_path)
            self.resize_image()

    def resize_image(self):
        '''
        The purpse of this function is to resize the image taken
        from the internet and resize it to the dimensions 300 x 300
        '''
        img = Image.open(self.image_path )
        img.size
        img = img.resize((300,300), Image.ANTIALIAS)
        img.size
        img.save(self.image_path ,'JPEG')



