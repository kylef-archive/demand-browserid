"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from demandapp.utils import normalise_site

class SimpleTest(TestCase):
    def test_normalise(self):
        self.assertEqual(normalise_site('www.heroku.com'), 'heroku.com')
        self.assertEqual(normalise_site('https://secure.gaug.es'), 'gaug.es')
        self.assertEqual(normalise_site('http://get.gaug.es/bla'), 'gaug.es')
        self.assertEqual(normalise_site('github.com/kylef'), 'github.com')

