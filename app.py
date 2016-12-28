############################################
####             IMPORTS                ####
############################################
from Tkinter import *
from PIL import Image, ImageTk
import ttk
import requests
import os
from scrape import Scrape
from fix_title import Fix
from music_db import MusicDB
from album_art import Art
from download_and_move import Download
import threading
import time

############################################
####             CLASSES                ####
############################################
Scrape = Scrape()
MusicDB = MusicDB()
Fx = Fix()
Art = Art()
dwn = Download()

class App(object):

    def run(self):
        
        self.root = Tk()
        self.root.title('Free Riddims')
        self.root.geometry('300x500')
        self.directory = 'C:\\Users\\User\\Documents\\python\\projects\\fr\\test_dir'
        
        s = ttk.Style()
        s.configure('.', background='white')

        mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        
        '''PERMANENT LABELS'''
        
        # LOGO LABEL 
        logo_img = ImageTk.PhotoImage(Image.open('art\\logo.jpg'))
        self.img_label = Label(mainframe, image=logo_img)
        self.img_label.grid(column=1, row=0, columnspan=2, sticky = S)
        
        # YOUTUBE ID ENTRY LABEL 
        youtube_id = StringVar()
        self.id_entry = ttk.Entry(mainframe, width=20, textvariable=youtube_id)
        self.id_entry.grid(column=1, row=1, columnspan=2, sticky=S)

        # DOWNLOAD BUTTON 
        self.log_button = ttk.Button(mainframe, text='Download', command=self.get_username)
        self.log_button.grid(column=1, row=2, columnspan=2, sticky = N)
        
        
        '''VARIABLE LABELS'''
        
        # SONG LABEL
        self.dwn_song = StringVar()
        self.song_label = Label(mainframe, textvariable=self.dwn_song)
        self.song_label.grid(column=2, row=4, sticky = (W,N))
        
        # ARTIST LABEL
        self.dwn_artist = StringVar()
        self.artist_label = Label(mainframe, textvariable=self.dwn_artist)
        self.artist_label.grid(column=2, row=5, sticky = (W,N)) 

        # ALBUM ART LABEL
        image_path = 'art\\no_art.jpg' 
        blank_image = Image.open(image_path)
        blank_image = blank_image.resize((100,100), Image.ANTIALIAS)
        tk_art_img = ImageTk.PhotoImage(blank_image)
        self.art_label = Label(mainframe, image=tk_art_img)
        self.art_label.grid(column=1, row=4, rowspan=3, sticky=(N,E)) 
        
        
        '''WEIGHTING'''
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        mainframe.columnconfigure(0, weight=3)
        mainframe.columnconfigure(1, weight=2)
        mainframe.columnconfigure(2, weight=2)
        mainframe.columnconfigure(3, weight=3)

        mainframe.rowconfigure(0, weight=1)
        mainframe.rowconfigure(1, weight=0)
        mainframe.rowconfigure(2, weight=0)
        mainframe.rowconfigure(3, weight=1)
        mainframe.rowconfigure(4, weight=0)
        mainframe.rowconfigure(5, weight=0)
        mainframe.rowconfigure(6, weight=1)
        mainframe.rowconfigure(7, weight=1)
        
        for child in mainframe.winfo_children(): child.grid_configure(padx=3, pady=5)
        self.id_entry.focus()
        self.root.bind('<Return>', self.get_username)
        
        ## MAKE BACKGROUNDS OF WIDGETS WHITE!!!
        
        self.root.mainloop()
        
    def get_username(self, *args):
        self.user_id = self.id_entry.get()
        if self.user_id == None:
            self.user_id = 'xxxx'
        self.check_user_id()
            
    def check_user_id(self):
        url = 'https://www.youtube.com/channel/' + self.user_id + '/playlists?sort=lad&view=1&flow=grid'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        request = requests.get(url, headers = headers)
        if request.status_code == 200:
            pass
        self.setup()
        self.start_download()
        
    def set_labels(self, song_info, image_path):
        self.dwn_song.set('Song :  ' + song_info[0])
        self.dwn_artist.set('Artist :  ' + song_info[1])
        dwn_art = Image.open(image_path)
        dwn_art = dwn_art.resize((100,100), Image.ANTIALIAS)
        tk_art_img = ImageTk.PhotoImage(dwn_art)
        self.art_label.configure(image=tk_art_img)
        self.art_label.image = tk_art_img
        self.root.update()
        
    def setup(self):
        if not os.path.isfile('db\\free_riddims.db'):
            MusicDB.create_database_structure()
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
            
    def start_download(self):
        t = threading.Thread(target=self.download_new_songs)
        print('starting main threads')
        t.start()

    def download_new_songs(self):
        self.playlists = Scrape.get_all_playlists('UC1eOi_4jVFP5IPnjogNiAWg')
        for i in self.playlists[0:2]:
             self.download_playlist(i)
        #self.download_playlist(self.playlists[0])


    def download_playlist(self, playlist):
        if not os.path.isdir(self.directory + '\\' + playlist[1]):
            os.makedirs(self.directory + '\\' + playlist[1])
        self.songs = Scrape.get_all_songs(playlist[0])
        previous_downloads = MusicDB.get_all_downloads()
        self.songs = [e for e in self.songs if e[0] not in previous_downloads]
        threads=[]
        for i in self.songs:
            #time.sleep(5)
            #t = threading.Thread(target=self.download_song, args=(i,playlist[1],))
            #threads.append(t)
            #print('starting mini trhread')
            #t.start()
            self.download_song(i,playlist[1])
        
    def download_song(self, song, playlist):
        song_info = Fx.fix_title(song[1])
        image_path = Art.get_album_art(song_info[1])
        self.set_labels(song_info, image_path)
        url = song[0]
        youtube_title = song[1]
        directory = self.directory
        song_name = song_info[0]
        artist = song_info[1]
        # Why can't I just use self?
        dwn.download_and_move(url, youtube_title, directory, playlist, song_name, artist, image_path)
        if dwn.song_downloaded:
            MusicDB.insert_download_data(url, youtube_title, playlist)
            MusicDB.insert_song_data(url, song_name, artist, playlist)
            print('song downloaded ' + song_name)
        else:
            print('song errored' + song_name)
            MusicDB.insert_errored_data( url, youtube_title, playlist)
        if artist is not None and image_path != 'album_art\\free_riddims_default.jpg':
            print('artist search successful '+artist)
            MusicDB.insert_artist_data(artist, image_path)


if __name__ == '__main__':
    app = App()
    app.run()