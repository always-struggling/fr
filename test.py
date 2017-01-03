import unittest
from music_db import MusicDB
from scrape import Scrape
from fix_title import Fix

class Setup(unittest.TestCase):

    def test_db(self):
        db = MusicDB()
        db.create_database_structure()
        db.insert_artist_data('Test Artist', None)
        db.insert_artist_data('MC RudeBoi', None)
        all_artists = db.get_all_artists()
        self.assertEqual(all_artists, [ 'Free Riddims','Test Artist', 'MC RudeBoi'])

class TestScraper(unittest.TestCase):

    def test_scrape_playlists(self):
        testcase_scrape = Scrape()
        playlists = testcase_scrape.get_all_playlists('UCztBf-iBKrDBYw4BzNK5B1Q')
        self.assertEqual(playlists, [ ('PLuXrQvHb49n4pHUoMYBLG5cVtrXhngcKR', 'playlist2')
                                    , ('PLuXrQvHb49n6jqOq9ftPHC8LVqDF5kG1X', 'playlist1')
                                    , ('LLztBf-iBKrDBYw4BzNK5B1Q', 'Likedvideos')
                                    ])

    def test_scrape_songs(self):
        testcase_scrape = Scrape()
        songs = testcase_scrape.get_all_songs('PLuXrQvHb49n4pHUoMYBLG5cVtrXhngcKR')
        self.assertEqual(songs,[ ('JRWox-i6aAk', 'Lana Del Rey - Blue Jeans')
                               , ('oKxuiw3iMBE', 'Lana Del Rey - West Coast')
                               ])

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
        self.assertEqual(split_title, ['Unknown Artist Some Song',''])

if __name__=='__main__':
    unittest.main()