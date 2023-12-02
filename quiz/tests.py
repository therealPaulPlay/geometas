from django.test import TestCase

from quiz.airtable_api import get_question


class AirtbaleAPITestCase(TestCase):
    
    def test_get_random_question(self):
        self.assertEqual(get_question(), 1)
        