import unittest
from app import app
from routes import secret_token

class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_add_book(self):
        response = self.client.post(
            "/books",
            headers={"x-access-token": secret_token},
            json={"title": "Sample Book", "author": "Author", "year": 2023},
        )
        self.assertEqual(response.status_code, 201)

    def test_get_books(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)

    def test_search_books(self):
        self.client.post(
            "/books",
            headers={"x-access-token": secret_token},
            json={"title": "Python Basics", "author": "John Doe", "year": 2023},
        )
        response = self.client.get("/books/search?q=python")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Python Basics" in response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
