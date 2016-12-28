############################################
####             IMPORTS                ####
############################################
from difflib import SequenceMatcher as SM 
from music_db import MusicDB
from titlecase import titlecase
import re

db = MusicDB()

############################################
####             CLASSES                ####
############################################

class Fix(object):

    '''
    This class fixes a youtube title. It removes any unwanted
    characters/words, and attempts to split the title into abs
    song name and artist. 
    '''



    def __init__(self):
        self.bad_words = [ 'full album'
                    , 'full version'
                    , 'full mixtape'
                    , 'full album stream'
                    , 'whole album'
                    , 'official video'
                    , 'official music video'
                    , 'official audio'
                    , 'hq audio'
                    , 'lyric video'
                    , 'hq'
                    , 'hd'
                    , 'good quality'
                    , 'high quality'
                    , 'teaser'
                    , 'flac'
                    , 'with lyrics'
                    , 'lyrics'
                    , 'original movie soundtrack'
                    , 'extended version'
                    , 'original speed master'
                    , 'original mix'
                    , 'live']

        self.all_artists = db.get_all_artists()

    def fix_title(self, youtube_title):
        '''
        This is the top level function for cleaning
        a youtube title. This function works in the following order:
            - Remove any unwanted words/characters
            - Attempt to split the song via a common delimiter
            - If we were unable to split the song via a delimiter
              we attempt to split it by a known artist
        '''
        self.youtube_title = youtube_title
        self.song_name = None
        self.artist = None
        self.title_split = False
        self.split_youtube_title = None
        self.remove_bad_words()

        self.split_song_via_delim()


        if self.title_split:
            self.sort_title()
        else:
            self.split_song_via_artist()

        if self.title_split:
            return (self.song_name, self.artist)
        else:
            return (self.youtube_title, '')

        
    def remove_bad_words(self):
        '''
        This function removes all bad words / characters / dates from the
        youtube title, and lowers it
        '''

                        
        '''Remove words (and any surrounding brackets) if they are in the bad words list''' 
        self.youtube_title = re.sub(r'([[|(]?(' + '|'.join(self.bad_words) + ').*[]|)]?)|(full)|(single)', '', self.youtube_title.lower() )    
        
        '''Remove any set of digits that could resemble a year'''
        self.youtube_title = re.sub(r'[[|(](1|2)\d{3}[]|)]','', self.youtube_title)
        
        '''Remove any characters that cause problems when saving the file'''
        self.youtube_title = re.sub('[#\/:*?"<>|]', '', self.youtube_title)
        
        
    def split_song_via_delim(self):
        '''
        We take the youtube title and we attempt to split it into artist and album. 
        Chance of success? High. Chance of perfection? Zero
        There seem to be three main delimiters in youtube titles:
           -   Your every day delimiter
           //  Your 'we're too different to follow convention' electronic music delimiter
           .   Your 'what?! who choses a fucking full stop. why is it common enough to have to be 
                     in this code. someone people are just rubbish at things' delimiter
                     
        In order of likelihood we try and split the song, check if it has been split into a list of two 
        elements.    
        '''

        title_delimiters = ['-', '//', '.']
        
        for delim in title_delimiters:
            if len(self.youtube_title.split(delim)) == 2:
                self.split_youtube_title = self.youtube_title.split(delim)
                self.split_youtube_title = [e.strip() for e in self.split_youtube_title]
                self.title_split = True
                break
       
    def sort_title(self):
        '''
        This function compares each value in the split youtube title to our list
        of known artists. It finds the best comparisson and if that comparisson is 
        greater than 0.7 (chosen by inspection), it sets self.artist as that matched
        artist. If no comparission is found then the self.artist is chosen as the 
        first element of the split title, and the song_name as the second element. 
        '''
        left_scores  = [ SM(None, self.split_youtube_title[0], e).ratio() for e in self.all_artists ]
        right_scores = [ SM(None, self.split_youtube_title[1], e).ratio() for e in self.all_artists ]
        if max(left_scores) < max(right_scores) and max (left_scores + right_scores) > 0.7:
            self.artist = self.split_youtube_title[1]
            self.song_name = self.split_youtube_title[0]
        else:
            self.artist = titlecase(self.split_youtube_title[0])
            self.song_name = titlecase(self.split_youtube_title[1])

    def split_song_via_artist(self):
        # NEEDS WORK
        # IF POSSIBLE_ARTISTS > 1
        '''
        If we are unable to split a song via a delimiter, we attempt 
        to split the song via a known artist. To do this, we get all our
        known artists from our database and attempt to split the title
        via the artist. If we only split the title by one artist then we know 
        the artist. If we split the title with more than one artist, then we know
        the artist if and only if all other artists are a subset of a single artist.
        '''
        possible_artists = [ e.lower() for e in self.all_artists if len(self.youtube_title.split(e.lower())) == 2 ]
        if len(possible_artists) == 1:
            self.title_split = True
            self.artist = titlecase(possible_artists[0] +  min(self.youtube_title.split(possible_artists[0]), key = len )).strip()
            self.song_name = titlecase(max(self.youtube_title.split(possible_artists[0]), key = len )).strip()


'''
setup = MusicDB()
setup.create_database_structure() 
setup.insert_artist_data('Kylie', 'album_art\\Kylie.jpg')
            
test = Fix()
song_info = test.fix_title('Adele - Hello(2015) High Quality')
print song_info
all_artists = test.get_all_artists()
print all_artists
song_info = test.fix_title('Kylie Slow')
print song_info
'''
    
