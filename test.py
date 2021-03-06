import unittest
import os
import shutil
from PIL import Image
from music_db import MusicDB
from scrape import Scrape
from fix_title import Fix
from album_art import Art
from download import Download
import os
from mutagen.easyid3 import EasyID3



class Setup(unittest.TestCase):
    def test_db(self):
        db = MusicDB()
        db.create_database_structure()
        db.insert_artist_data('Test Artist', '/test_path/test_artist.jpg')
        db.insert_artist_data('MC RudeBoi', None)
        all_artists = db.get_all_artists()
        self.assertEqual(all_artists, ['Free Riddims', 'MC RudeBoi', 'Test Artist'])


class TestFixer(unittest.TestCase):
    def test_fix_by_delimiter(self):
        testcase_fix = Fix()
        split_song = testcase_fix.split_song_via_delim('Test Artist - Test Song')
        self.assertEqual(split_song, ['Test Artist', 'Test Song'])
        split_song = testcase_fix.split_song_via_delim('Test Artist // Test Song')
        self.assertEqual(split_song, ['Test Artist', 'Test Song'])
        split_song = testcase_fix.split_song_via_delim('TEST ARTIST . TEST SONG')
        self.assertEqual(split_song, ['Test Artist', 'Test Song'])
        split_song = testcase_fix.split_song_via_delim('TEST ARTIST TEST SONG')
        self.assertEqual(split_song, ['TEST ARTIST TEST SONG', ''])

    def test_sort_title(self):
        testcase_fix = Fix()
        sorted_title = testcase_fix.sort_title(['Test Artist', 'Test Song'])
        self.assertEqual(sorted_title, ['Test Artist', 'Test Song'])
        sorted_title = testcase_fix.sort_title(['Test Song', 'Test Artist'])
        self.assertEqual(sorted_title, ['Test Artist', 'Test Song'])
        sorted_title = testcase_fix.sort_title(['Test Song', 'Some Other Artist'])
        self.assertEqual(sorted_title, ['Test Song', 'Some Other Artist'])

    def test_split_song_via_artist(self):
        testcase_fix = Fix()
        split_title = testcase_fix.split_song_via_artist('Test Artist Test Song')
        self.assertEqual(split_title, ['Test Artist', 'Test Song'])
        split_title = testcase_fix.split_song_via_artist('TEST SONG TEST ARTIST')
        self.assertEqual(split_title, ['Test Artist', 'Test Song'])
        split_title = testcase_fix.split_song_via_artist('MC RudeBoi  Garage Beats')
        self.assertEqual(split_title, ['Mc Rudeboi', 'Garage Beats'])
        split_title = testcase_fix.split_song_via_artist('Unknown Artist Some Song')
        self.assertEqual(split_title, ['Unknown Artist Some Song', ''])

    def test_fix_title(self):
        testcase_fix = Fix()
        artist, song = testcase_fix.fix_title('Test Artist - Test Song')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('TEST ARTIST - TEST SONG')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('Test Song - Test Artist')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('TEST SONG - TEST ARTIST')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('Test Artist Test Song')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('TEST ARTIST TEST SONG')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('Test Song Test Artist')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')
        artist, song = testcase_fix.fix_title('TEST SONG TEST ARTIST')
        self.assertEqual(song, 'Test Song')
        self.assertEqual(artist, 'Test Artist')


class TestScraper(unittest.TestCase):
    def test_scrape_playlists(self):
        testcase_scrape = Scrape()
        playlists = testcase_scrape.get_all_playlists('UCztBf-iBKrDBYw4BzNK5B1Q')
        self.assertEqual(playlists, [['PLuXrQvHb49n4pHUoMYBLG5cVtrXhngcKR', 'playlist2']
            , ['PLuXrQvHb49n6jqOq9ftPHC8LVqDF5kG1X', 'playlist1']
            , ['LLztBf-iBKrDBYw4BzNK5B1Q', 'Likedvideos']
                                     ])

    def test_scrape_songs(self):
        testcase_scrape = Scrape()
        songs = testcase_scrape.get_all_songs('PLuXrQvHb49n4pHUoMYBLG5cVtrXhngcKR')
        self.assertEqual(songs, [['JRWox-i6aAk', 'Lana Del Rey - Blue Jeans']
            , ['oKxuiw3iMBE', 'Lana Del Rey - West Coast']
                                 ])

    def test_scrape_all_songs(self):
        testcase_scrape = Scrape()
        songs = testcase_scrape.set_youtube_songs('UCztBf-iBKrDBYw4BzNK5B1Q')
        self.assertEqual(songs, [['JRWox-i6aAk', 'Lana Del Rey - Blue Jeans', 'playlist2']
            , ['oKxuiw3iMBE', 'Lana Del Rey - West Coast', 'playlist2']
            , ['_z-1fTlSDF0', 'Happy Birthday song', 'playlist1']
            , ['Bag1gUxuU0g', 'Lana Del Rey - Born To Die', 'playlist1']
            , ['vrlTeoFcf-Q', '[Private video]', 'Likedvideos']
                                 ])


class TestArt(unittest.TestCase):
    def test_search_existing_art(self):
        db = MusicDB()
        all_art = dict(db.get_all_art())
        art = (all_art['Test Artist'])
        self.assertEqual('/test_path/test_artist.jpg', art)

    def test_get_art_url_found(self):
        art = Art()
        image_url, image_path_found = art.find_art2('bowie')
        self.assertEqual(image_url, 'https://images-na.ssl-images-amazon.com/images/I/618%2Bo-mU-sL.jpg')
        self.assertEqual(image_path_found, True)

    def test_get_art_url_not_found(self):
        art = Art()
        image_url, image_path_found = art.find_art2('kjgsogaghg')
        self.assertEqual(image_url, '')
        self.assertEqual(image_path_found, False)

    def test_download_art(self):
        art = Art()
        art.download_image('https://images-na.ssl-images-amazon.com/images/I/31inGXqqWsL.jpg', 'bowie')
        self.assertEqual(os.path.isfile('album_art\\bowie.jpg'), True)
        os.remove('album_art\\bowie.jpg')

    def test_resize_image(self):
        art = Art()
        art.resize_image('album_art\\free_riddims_default.jpg')
        img = Image.open('album_art\\free_riddims_default.jpg')
        self.assertEqual(img.size, (300, 300))

    def test_get_image_known(self):
        art = Art()
        image_path = art.get_album_art('bowie')
        self.assertEqual(image_path, 'album_art\\bowie.jpg')
        os.remove('album_art\\bowie.jpg')

    def test_get_image_found(self):
        art = Art()
        image_path = art.get_album_art('adele')
        self.assertEqual(image_path, 'album_art\\adele.jpg')
        os.remove('album_art\\adele.jpg')

    def test_get_image_not_found(self):
        art = Art()
        image_path = art.get_album_art('dslfknsdlg')
        self.assertEqual(image_path, 'album_art\\free_riddims_default.jpg')


class TestDownload(unittest.TestCase):
    def test_1_download_song(self):
        dwn = Download()
        dwn.download_song('NCFg7G63KgI')
        self.assertEqual(os.path.isfile('The funniest 10 second video ever-NCFg7G63KgI.mp3'), True)
        os.remove('The funniest 10 second video ever-NCFg7G63KgI.mp3')

    def test_2_append_tags(self):
        dwn = Download()
        shutil.copy('music_test\\test.mp3', 'test_append.mp3')
        filename = os.getcwd() + '\\test_append.mp3'
        art = 'C:\\Users\\User\\Documents\\python\\projects\\fr\\album_art\\free_riddims_default.jpg'
        appended_mp3 = EasyID3(filename)
        dwn.append_tags(filename, 'Test Song', 'Test Artist', 'Test Playlist', art)
        self.assertEqual(appended_mp3['title'][0], 'Test Song')
        self.assertEqual(appended_mp3['artist'][0], 'Test Artist')
        self.assertEqual(appended_mp3['album'][0], 'Test Playlist')

        os.remove(filename)

    def test_3_move_song(self):
        dwn = Download()
        shutil.copy('music_test\\test.mp3', 'test_move.mp3')
        tmp_filename = os.getcwd() + '\\test_move.mp3'
        new_filename = os.getcwd() + '\\music_test\\test move.mp3'
        dwn.move_song(tmp_filename, new_filename)
        self.assertEqual(os.path.isfile('music_test\\test move.mp3'), True)
        os.remove('music_test\\test move.mp3')

    def test_4_get_song(self):
        dwn = Download()
        dwn.get_song('NCFg7G63KgI', 'The funniest 10 second video ever', 'test song', 'test artist', 'test playlist', 'album_art\\free_riddims_default.jpg')
        self.assertEqual(os.path.isfile('music_test\\test song.mp3'), True)
        os.remove('music_test\\test song.mp3')

if __name__ == '__main__':
    unittest.main()
