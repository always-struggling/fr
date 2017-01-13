############################################
####             IMPORTS                ####
############################################
import sqlite3
import os



############################################
####             CLASSES                ####
############################################


class MusicDB(object):

    '''
    This class provides the functions for connecting to and
    interacting with the local database. As well as the functions for 
    creating the databse structure, that is used throughout the project
    
    The tables of the database are:
      - DOWNLOADED_SONGS [ YOUTUBE_URL | YOUTUBE_TITLE ]
      - ERRORED_SONGS [ YOUTUBE_URL | YOUTUBE_TITLE ]
      - ARTISTS [ ARTIST | ALBUM_ART_PATH ]
      - SONGS [ YOUTUBE_URL | SONG_NAME | ARTIST | ALBUM ]

    '''

    def connect(self):
        self.conn = sqlite3.connect( os.getcwd() + '\\db\\free_riddims.db')
        self.c = self.conn.cursor()
        
        
    def create_database_structure(self):
        self.connect()
        # USERS #
        try:
            self.c.execute('''DROP TABLE USERS''')
        except:
            pass
        self.c.execute('''CREATE TABLE USERS ( USER_ID VARCHAR2(100) PRIMARY KEY NOT NULL
                                              , DIRECTORY_PATH VARCHAR2(300) )''') 
    
        # DOWNLOADED_SONGS #
        try:
            self.c.execute('''DROP TABLE DOWNLOADED_SONGS''')
        except sqlite3.OperationalError:
            pass
        self.c.execute('''CREATE TABLE DOWNLOADED_SONGS ( YOUTUBE_URL VARCHAR2(200) PRIMARY KEY NOT NULL
                                                        , YOUTUBE_TITLE VARCHAR2(200) NOT NULL
                                                        , PLAYLIST VARCHAR2(100))''')

        # ERRORED_SONGS #
        try:
            self.c.execute('''DROP TABLE ERRORED_SONGS''')
        except sqlite3.OperationalError:
            pass
        self.c.execute('''CREATE TABLE ERRORED_SONGS ( YOUTUBE_URL VARCHAR2(200) PRIMARY KEY NOT NULL
                                                     , YOUTUBE_TITLE VARCHAR2(200) NOT NULL 
                                                     , PLAYLIST VARCHAR2(100)) ''')
        
        # SONGS #                    
        try:
            self.c.execute('''DROP TABLE SONGS''')
        except sqlite3.OperationalError:
            pass
        self.c.execute('''CREATE TABLE SONGS( YOUTUBE_URL VARCHAR2(200) PRIMARY KEY NOT NULL
                                            , SONG_NAME VARCHAR2(200) NOT NULL
                                            , ARTIST VARCHAR2(200)
                                            , PLAYLIST VARCHAR2(200)
                                            , FOREIGN KEY (YOUTUBE_URL) REFERENCES DOWNLOAD_SONGS (YOUTUBE_URL) )''')

        # ARTISTS #        
        try:
            self.c.execute('''DROP TABLE ARTISTS''')
        except sqlite3.OperationalError:
            pass
        self.c.execute('''CREATE TABLE ARTISTS( ARTIST VARCHAR2(200) PRIMARY KEY NOT NULL
                                              , ARTIST_ART_PATH VARCHAR2(1000) UNIQUE )''')
                                              
        
        '''
        We have to insert one value into our artists table. This is the information
        for the free riddims default image. If we do not include this insert, the album
        path will be inserted later on without an artist. Then when we try to split
        by artist in fix_title.py, we get an empty seperator errored_songs
        '''
        self.insert_artist_data('Free Riddims', 'album_art_free_riddims_default.jpg')
        
    
    def insert_errored_data(self, url, youtube_title, playlist):
        '''
        Inserts failed downloads into ERRORED_SONGS 
        '''
        self.connect()
        insert = [(url, youtube_title, playlist)]
        self.c.executemany('''insert into errored_songs values ( ?, ?, ?)''', insert)
        self.conn.commit()           
 
    def insert_download_data(self, url, youtube_title, playlist):
        '''
        Inserts successfully downloaded youtube videos into DOWNLOADED_SONGS
        '''
        self.connect()
        insert = [(url, youtube_title, playlist)]
        self.c.executemany('''insert into downloaded_songs values ( ?, ?, ?)''', insert)
        self.conn.commit() 
        
    def insert_song_data(self, url, song_name, artist, playlist):
        '''
        Inserts fixed song titles and artists into SONGS
        '''
        self.connect()
        insert = [(url, song_name, artist, playlist)]
        self.c.executemany('''insert into songs values ( ?, ?, ?, ?)''', insert)
        self.conn.commit()
        
    def insert_artist_data(self, artist, image_path):
        '''
        Inserts artist information into the ARTISTS table if we do not already have it.
        '''
        self.connect()
        self.c.execute('''select artist_art_path from artists where artist = ?''', [artist]) 
        result = self.c.fetchone()
        if result is None:
            insert = [(artist, image_path)]
            self.c.executemany('''insert into artists values (?, ?)''', insert)
        elif result[0] is None:
            update = [(image_path, artist)]
            self.c.executemany ('''update artists 
                                      set artist_art_path = ? 
                                    where artist = ? ''', update)
        self.conn.commit() 

            
    def get_all_artists(self):
        '''
        This function gets all the artists we have previously downloaded and
        inserted into the database. 
        '''
        self.connect()
        self.c.execute('''select artist from artists order by artist''')
        self.all_artists = self.c.fetchall()
        self.all_artists = [e[0] for e in self.all_artists] 
        # if artists is null we cause problems when trying to iterate
        # through an empty set. A small hack to get round this problem is to do:
        if self.all_artists == []:
             self.all_artists = ['free riddims - dummy value']
        return self.all_artists
        
    def get_all_downloads(self):
        '''
        This function gets all the songs we have previously downloaded and
        inserted into the database. 
        '''        
        self.connect()
        self.c.execute('''select YOUTUBE_URL from downloaded_songs
                               UNION
                          select YOUTUBE_URL from errored_songs''') 
        result = self.c.fetchall()
        all_songs = [e[0] for e in result]
        if all_songs == []:
             all_songs = ['free riddims - dummy value']
        return all_songs

             
    def get_all_art(self):
        '''
        This function checks the ARTISTS table and returns the image path 
        for the artist art if it exists. 
        NOTE - sqlite:
            If we run the query 'select A from B where C = c' and:
               - A is null and c exists in B then we return (None, )
               - c does not exist in B then we return None
        '''        
        self.connect()
        self.c.execute('''select artist, artist_art_path from artists where artist_art_path is not null''')
        result = self.c.fetchall()
        return result


'''     
url = '12345'
youtube_title = 'Tester - Test'
song_name = 'Test'
playlist = 'Testlist'


artist_1 = 'artist_1'
artist_2 = 'artist_2'
artist_3 = 'artist_3'
image_path_1 = 'C:\\Path_1'
image_path_2 = None

test = MusicDB()
test.create_database_structure() 
file_exists = os.path.isfile('C:\\\\Users\\User\\Documents\\python\\projects\\you_dl\\you_dl\\new\\db\\test.db' )
print file_exists
tables = test.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = test.c.fetchall()
print tables 
test.insert_errored_data(url, youtube_title, playlist)
result = test.c.execute("SELECT * FROM ERRORED_SONGS")
result = test.c.fetchall()
print result
test.insert_download_data(url, youtube_title, playlist)
result = test.c.execute("SELECT * FROM DOWNLOADED_SONGS")
result = test.c.fetchall()
print result
test.insert_song_data(url, song_name, artist_1, playlist)
result = test.c.execute("SELECT * FROM SONGS")
result = test.c.fetchall()
print result

test.insert_artist_data(artist_1, image_path_1)
test.insert_artist_data(artist_2, image_path_2)
test.insert_artist_data(artist_3, image_path_2)

image_path_2 = 'C:\Path_2'

test.insert_artist_data(artist_2, image_path_2)
test.insert_artist_data(artist_2, image_path_2)


result = test.c.execute("SELECT * FROM ARTISTS")
result = test.c.fetchall()
print 'all artists'
print result
art_path = test.get_art_via_artist('artist_1')
print art_path
art_path = test.get_art_via_artist('artist_2')
print art_path
art_path = test.get_art_via_artist('artist_3')
print art_path
'''

