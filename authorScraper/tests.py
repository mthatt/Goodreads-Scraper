from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId
from app import app

class PlaylistsTests(TestCase):
    """Flask tests."""
    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_get_book(self):
        """Test the playlists homepage."""
        result = self.client.get('/book?id=604a5befce4f16ca6e06da12')
        self.assertEqual(result.status, '200 OK')

    def test_get_author(self):
        """Test the playlists homepage."""
        result = self.client.get('/author?id=604a5ce019081ce591f6f746')
        self.assertEqual(result.status, '200 OK')

    def test_post_author(self):
        """Test the playlists homepage."""
        result = self.client.post('/author', json={
            "name":"Tester2",
            "author_url":"jdoe222123",
            "rating":"2.34",
            "rating_count":"242",
            "review_count":"32",
            "image_url":"testurl426"
        })
        self.assertEqual(result.status, '200 OK')

    def test_post_book(self):
        """Test the playlists homepage."""
        result = self.client.post('/book', json={
            "title":"Tester2",
            "book_url":"test222url1234",
            "author_url":"jdoe222123",
            "author":"John222",
            "rating":"4.3222",
            "rating_count":"24222",
            "review_count":"36222",
            "image_url":"testyrl452226"
        })
        self.assertEqual(result.status, '200 OK')

    def test_post_books(self):
        """Test the playlists homepage."""
        result = self.client.post('/books', json=[{
            "title":"Tester87",
            "book_url":"test222url1234",
            "author_url":"jdoe222123",
            "author":"John222",
            "rating":"4.3222",
            "rating_count":"24222",
            "review_count":"36222",
            "image_url":"testyrl452226"},
            {
            "title":"Tester543",
            "book_url":"testurl1233334",
            "author_url":"jdoe333123",
            "author":"John333",
            "rating":"4.3333",
            "rating_count":"24333",
            "review_count":"36333",
            "image_url":"testyrl433356"}])
        self.assertEqual(result.status, '200 OK')

    def test_post_authors(self):
        """Test the playlists homepage."""
        result = self.client.post('/authors', json=[{
            "name":"Tester2",
            "author_url":"jdoe222123",
            "rating":"2.34",
            "rating_count":"242",
            "review_count":"32",
            "image_url":"testurl426"},
            {
            "name":"Tester2",
            "author_url":"jdoe222123",
            "rating":"2.34",
            "rating_count":"242",
            "review_count":"32",
            "image_url":"testurl426"}])
        self.assertEqual(result.status, '200 OK')

    def test_delete_author(self):
        result = self.client.delete('/author?id=604a5ce019081ce591f6f746')
        self.assertEqual(result.status, '200 OK')

    def test_delete_book(self):
        result = self.client.delete('/book?id=604a5befce4f16ca6e06da12')
        self.assertEqual(result.status, '200 OK')

    def test_delete_book_badid_error(self):
        result = self.client.delete('/book?id=604662e9c')
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_delete_author_badid_error(self):
        result = self.client.delete('/author?id=604664232e9c')
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_get_book_badid_error(self):
        """Test the playlists homepage."""
        result = self.client.get('/book?id=60466178c26be79896')
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_get_author_badid_error(self):
        """Test the playlists homepage."""
        result = self.client.get('/author?id=60be79896')
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_put_author_badid_error(self):
        result = self.client.put('/author?id=60be79896')
        self.assertEqual(result.status, '404 NOT FOUND')

    def test_put_book_badid_error(self):
        result = self.client.put('/book?id=60be79896')
        self.assertEqual(result.status, '404 NOT FOUND')

    # def test_put_book(self):
    #     result = self.client.put('/book?id=604a5befce4f16ca6e06da12')
    #     self.assertEqual(result.status, '200 OK')
    #
    # def test_put_author(self):
    #     result = self.client.put('/author?id=604a5ce019081ce591f6f746')
    #     self.assertEqual(result.status, '200 OK')

if __name__ == '__main__':
    unittest_main()