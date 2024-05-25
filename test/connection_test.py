
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from app import app # Flask instance of the API
import unittest

class TestEncoder(unittest.TestCase):

    def test_index_route(self):
        response = app.test_client().get('/')

        assert response.status_code == 200
        assert response.data.decode('utf-8') == 'App is working'


if __name__ == '__main__':
    unittest.main()