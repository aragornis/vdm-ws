from posts.repository import Post
import html
from dateutil import parser
from dateutil import tz
import re

class Parser:
    """ Provide parsing of a vdm page to a list of embed posts as Post objects. """
    def __init__(self):
        self.__regex = re.compile('<div class="post article" id="\d+"><p>(.*?)<\/p><div class="date"><div class="left_part">.*?<p>Le ([^-]*?) - .*? - par (.*?) (\(<a.*?<\/a>\))?<\/p><\/div>', re.MULTILINE)

    def parse(self, page):
        """ Parse provided page represented as a string and return contained posts as a list of Post objects. """
        return [self.__createPostFromMatch(m) for m in self.__regex.findall(page)]

    def __createPostFromMatch(self, match):
        return Post(match[2], self.__cleanupDescription(match[0]), self.__parseDate(match[1]))

    def __cleanupDescription(self, desc):
        return re.sub('<[^<]*?>', '', html.unescape(desc))

    def __parseDate(self, date):
        return parser.parse(date.replace('\u00e0', ''), dayfirst = True).replace(tzinfo= tz.gettz('Europe/Paris'))
