############################################
####             IMPORTS                ####
############################################
from bs4 import BeautifulSoup
import requests
import json
import re


############################################
####             CLASSES                ####
############################################


class Scrape(object):
    '''
    This class holds the functions for scraping a users playlist titles
    and playlist urls, as well as the song titles and song urls in a 
    playlist. 
    '''

    def set_youtube_songs(self, user_id):
        '''
        This scrapes the entire youtube library of the user
        :param user_id: The youtube_id for the user
        :return: a nested list of [youtube_title, youtube_url, playlist]
        '''
        playlists = self.get_all_playlists(user_id)
        songs = []
        for playlist in playlists:
            songs = songs + [e + [playlist[1]] for e in self.get_all_songs(playlist[0])]
        return songs

    def find_load_more_url(self, soup):
        '''
        Youtube uses Javascript to load additonal artists. 
        This function determine is there is more of the webpage to load,
        and returns the url to load it.
        '''
        for button in soup.find_all("button"):
            url = button.get("data-uix-load-more-href")
            if url:
                return "http://www.youtube.com" + url

                
    def scrape_playlist_page(self, soup):
        '''
        This functions scrapes the titles and urls of each playlist 
        on a specific playlist webpage and retruns them as a list of tuples.
        '''
        playlist_html = soup.find_all('div', {'class':'yt-lockup-content'})
        playlist_titles = [e.contents[1].find_all('a', {'class':'yt-uix-sessionlink'})[0].text.replace(' ','') 
                                for e in playlist_html]
        playlist_urls = [e.contents[1].find_all('a', {'class':'yt-uix-sessionlink'})[0].get('href')
                                for e in playlist_html]
        playlist_urls = [e.replace('/playlist?list=', '') for e in playlist_urls]
        playlists = [list(e) for e in zip(playlist_urls, playlist_titles)]
        return playlists
        
        
    def get_all_playlists(self, user_id):
        '''
        This function returns all playlist titles and urls 
        for a specific user.
        '''
        url = 'https://www.youtube.com/channel/' + user_id + '/playlists?sort=lad&view=1&flow=grid'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = requests.get(url, headers = headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        all_playlists = self.scrape_playlist_page(soup)
        load_more_url = self.find_load_more_url(soup)
        while load_more_url:
            html = requests.get(load_more_url).text
            json_data = json.loads(html)
            soup = BeautifulSoup(json_data.get("content_html", ""), 'html.parser')
            all_playlists = all_playlists + self.scrape_playlist_page(soup)
            load_more_url = self.find_load_more_url(BeautifulSoup(json_data.get('load_more_widget_html',''), 'html.parser'))
        return all_playlists

    def scrape_songs_page(self, soup):
        '''
        This function scrapes the song titles and urls,
        and returns them as a list of tuples.
        '''
        song_html = soup.find_all('a', {'class':'pl-video-title-link'})
        song_urls = [e.get('href') for e in song_html]
        song_urls = [re.findall('^[^&]*', e)[0] for e in song_urls]
        song_urls = [e.replace('/watch?v=','') for e in song_urls]
        song_titles = [e.text[7:len(e)-6] for e in song_html]
        songs = [list(e) for e in zip(song_urls, song_titles)]
        return songs  

    def get_all_songs(self, url):
        '''
        This functions returns all the song titles and urls
        in a playlist.
        '''
        url = 'http://www.youtube.com/playlist?list=' + url
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        html = requests.get(url, headers = headers)
        soup = BeautifulSoup(html.content, 'html.parser')
        all_songs = self.scrape_songs_page(soup)
        load_more_url = self.find_load_more_url(soup)
        while load_more_url:
            html = requests.get(load_more_url).text
            json_data = json.loads(html)
            soup = BeautifulSoup(json_data.get("content_html", ""), 'html.parser')
            all_songs = all_songs + self.scrape_songs_page(soup)
            load_more_url = self.find_load_more_url(BeautifulSoup(json_data.get('load_more_widget_html',''), 'html.parser'))  
        return all_songs        

        
if __name__ == '__main__':
    scrape = Scrape()
    playlists = scrape.get_all_playlists('UCztBf-iBKrDBYw4BzNK5B1Q')
    print (playlists)


        