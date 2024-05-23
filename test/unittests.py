
import unittest
from flask import Flask
from app import app

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()

    def test_document_search_route(self):
        # Тестирование успешного поиска документов по запросу
        response = self.app.get('/documents?query=test')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)  # Проверка на наличие результатов

        # Тестирование поиска без указания запроса
        response = self.app.get('/documents')
        self.assertEqual(response.status_code, 400)

    def test_indices_search_route(self):
        # Тестирование успешного поиска индексов по запросу
        response = self.app.get('/indexes?query=test')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)  # Проверка на наличие результатов

        # Тестирование поиска без указания запроса
        response = self.app.get('/indexes')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
