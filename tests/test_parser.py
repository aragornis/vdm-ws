import unittest
import os
import codecs
from crawler.parser import Parser
from datetime import datetime
from dateutil import tz

class ParserTests(unittest.TestCase):
    def setUp(self):
        self._parser = Parser()

    def test_empty(self):
        result = self._parser.parse('')
        self.assertEqual(len(result), 0)

    def test_sample_page(self):
        with codecs.open(os.path.join(os.path.dirname(__file__), 'vdm_sample.html'), 'r', 'utf-8') as f:
            data = f.read()
        result = self._parser.parse(data)

        self.assertEqual(len(result), 13)

        post = result[0]
        self.assertEqual(post.author, 'Jbln!')
        self.assertEqual(post.date, datetime(2016, 1, 9, 16, 33, tzinfo = tz.gettz('Europe/Paris')))
        self.assertEqual(post.content, "Aujourd'hui, je reçois une lettre d'invitation à un mariage ! Celui de ma \"meilleure\" amie qui m'a piqué mon mec lorsque que je l'ai accueillie chez moi après une de ses ruptures. Petit plus, elle me demande d'être une de ses demoiselles d'honneur. VDM")

        post = result[1]
        self.assertEqual(post.author, 'ivegotnomoney')
        self.assertEqual(post.date, datetime(2016, 1, 9, 14, 12, tzinfo = tz.gettz('Europe/Paris')))
        self.assertEqual(post.content, "Aujourd'hui, comme depuis des années maintenant, mes parents tiennent toujours à la règle de \"celui qui obtient la fève rembourse la galette des rois\". Étant en repas de famille nombreuse, il y a donc trois galettes. J'ai eu les trois fèves et je suis une étudiante avec un budget très serré. VDM")