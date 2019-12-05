import unittest
from app import app


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page_test(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_error_handler(self):
        result = self.app.get('/garbage')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
