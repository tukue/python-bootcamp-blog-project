import unittest
from main import app

class MainTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_all_posts(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def  test_about_post(self):
        response = self.app.get('/about', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def  test_contact_post(self):
        response = self.app.get('/contact', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    if __name__ == "__main__":
    unittest.main(verbosity=2)
