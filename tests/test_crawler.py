import unittest
import os
import codecs
from crawler.parser import Parser
from crawler.crawler import Crawler
from datetime import datetime
from dateutil import tz

class FetcherMock():
    def __init__(self, contentGenerator):
        self.__contentGenerator = contentGenerator

    def downloadPage(self, page_index):
        return self.__contentGenerator(page_index)

class ParserMock():
    def parse(self, page):
        return page

class CrawlerTests(unittest.TestCase):
    def test_fail_on_empty_result(self):
        # Checks raising when a page is empty
        crawler = Crawler(FetcherMock(lambda x: range(3) if x == 0 else []), ParserMock())
        self.assertRaises(StopIteration, crawler.crawl, 5)

    def test_lucky_path(self):
        # Simulates parsed pages with posts represented by ints in range [page_index*7, page_index*7+7[
        crawler = Crawler(FetcherMock(lambda x: range(x*7, (x+1)*7)), ParserMock())

        # Check when number of posts is not a multiple of posts per page
        result = crawler.crawl(32)
        self.assertEqual(result, list(range(32)))

        # Check when number of posts is a multiple of posts per page
        result = crawler.crawl(21)
        self.assertEqual(result, list(range(21)))