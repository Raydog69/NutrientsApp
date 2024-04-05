from website import create_app
import unittest

app = create_app()

class MyTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home(self):
        result = self.app.get('/')
        self.assertEqual(app.testing, result)

if __name__ == '__main__':
    unittest.main()
    app.run(debug=True)
