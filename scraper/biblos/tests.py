from django.test import TestCase
from .scraper.scraper import extract_data
import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraper.settings'
django.setup()

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'test_utils/articles.html')


class TestCases(TestCase):
    
    
    def setUp(self):
       self.testfile = open(TESTDATA_FILENAME)
       self.testdata = self.testfile.read()

    def tearDown(self):
       self.testfile.close()
    
    
    def test_creating_objects(self):
        # Creating objects out of raw html
        articles = extract_data(self.testdata)
        self.assertEqual(20, len(articles), msg=f"len(articles) == 20")
   
    def test_extracting_fields(self):
        title = 'Computer aided design of components for energy transfer : Local LNG station'
        authors = ['Lisowski, Edward', 'Czyżycki, Wojciech', 'Filo, Grzegorz']
        type = 'książka'
        release_date = 2013
        
        # Creating objects out of raw html
        articles = extract_data(self.testdata)

        self.assertEqual(articles[0].title,title, msg=f"articles[0].title == title")
        self.assertEqual(len(articles[0].authors),len(authors), msg=f"len(articles[0].authors) == len(authors)")
        self.assertIn(type,articles[0].typ, msg=f"articles[0].type == type")
        self.assertEqual(release_date,int(articles[0].release_date), msg=f"articles[0].release_date == release_date")        
        
   