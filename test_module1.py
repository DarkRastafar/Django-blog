from unittest import TestCase
import requests


class SoloFunctionsTestCase(TestCase):
    def test_test(self):
        print('Assert complete!')
        self.assertEqual(1, 1)

    def test_russian_chr(self):
        print('Тест')
        self.assertEqual('Тест', 'Тест')

    def test_requests(self):
        print(requests.Request)

