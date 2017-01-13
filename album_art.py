############################################
####             IMPORTS                ####
############################################
from music_db import MusicDB
from bs4 import BeautifulSoup
from PIL import Image
import urllib as dwn
import requests


class Art(object):
    '''
    This class contains the functions for retrieving
    album art for an artist
    '''

    def __init__(self):

        db = MusicDB()
        self.all_art = dict(db.get_all_art())
        self.default_image = 'album_art\\free_riddims_default.jpg'

    def get_album_art(self, artist):
        '''
        This function is the top level function for retrieving
        album art for an artist. It takes an artist as a parameter
        and searches the database for the image path of an existing
        image If none exists, it then attempts to scrape one from the
        internet. If we are still unable to find one it returns the default
        free riddims album art.
        '''
        if artist == '':
            return self.default_image

        try:
            image_path = self.all_art[artist]
        except:
            image_url, image_url_found = self.find_art2(artist)
            if image_url_found:
                self.download_image(image_url, artist.replace(' ', '_').lower())
                self.resize_image('album_art\\' + artist.replace(' ', '_').lower() + '.jpg')
                image_path = 'album_art\\' + artist.replace(' ','_').lower() + '.jpg'
            else:
                image_path = self.default_image
        return image_path

    def find_art1(self, artist):
        '''
        This function attempts to scrape an album cover from
        the website www.covermytumes.com
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = 'http://www.covermytunes.com/search.php?search_query=' + artist.replace(' ', '+') + '&x=0&y=0'
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        if len(soup.find_all('h2')) == 0:
            image_urls = soup.find_all('img')
            image_urls = [(e.get('src'), e.get('height'), e.get('width')) for e in image_urls]
            image_url = image_urls[0][0]
            image_url_found = True
        else:
            image_url = ''
            image_url_found = False
        return image_url, image_url_found

    def find_art2(self, artist):
        '''
        This function attempts to scrape an album cover from
        the website www.seekacover.com
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url = 'http://www.seekacover.com/cd/' + artist.replace(' ', '+')
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        image_urls = [e.get('src') for e in soup.find_all('img')[2:]]
        if len(image_urls) > 2:
            image_url = image_urls[0]
            image_found = True
        else:
            image_url = ''
            image_found = False
        return image_url, image_found

    def download_image(self, image_url, artist):
        dwn.urlretrieve(image_url, 'album_art\\' + artist.lower().replace(' ','_') + '.jpg')

    def resize_image(self, image_path):
        '''
        The purpose of this function is to resize the image taken
        from the internet and resize it to the dimensions 300 x 300
        '''
        img = Image.open(image_path)
        img = img.resize((300,300), Image.ANTIALIAS)
        img.save(image_path, 'JPEG')



