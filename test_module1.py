from unittest import TestCase


class SoloFunctionsTestCase(TestCase):
    def test_test(self):
        print('Assert complete!')
        self.assertEqual(1, 1)

    def test_russian_words(self):
        print('Тест')
        self.assertEqual('Тест', 'Тест')
