import server
import unittest
from posts.repository import *
import json
from dateutil import tz

class ServerTests(unittest.TestCase):

    def setUp(self):
        server.server.config['TESTING'] = True
        self.app = server.server.test_client()
        server.repository = Posts(':memory:', True)
        server.repository.addPost(Post('0', 1, datetime(2015, 5, 1, tzinfo = tz.gettz('Europe/Paris'))))
        server.repository.addPost(Post('0', 2, datetime(2015, 5, 3, tzinfo = tz.gettz('Europe/Paris'))))
        server.repository.addPost(Post('1', 3, datetime(2015, 5, 5, tzinfo = tz.gettz('Europe/Paris'))))

    def test_getAllPosts(self):
        response = self.app.get('/api/posts')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['count'], 3)
        self.assertEqual(len(data['posts']), 3)

    def test_getAllPosts_NoResult(self):
        response = self.app.get('/api/posts?from=2016-01-01')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['count'], 0)
        self.assertEqual(len(data['posts']), 0)

    def test_getAllPosts_Filter(self):
        response = self.app.get('/api/posts?to=2015-05-04&from=2015-05-02&author=0')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['posts'], [{'author': '0', 'content': 2, 'date': '2015-05-03 00:00:00', 'id': 1}])

    def test_getPost(self):
        response = self.app.get('/api/post/1')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data['post'], {'author': '0', 'content': 2, 'date': '2015-05-03 00:00:00', 'id': 1})

    def test_getPost_Unknown(self):
        response = self.app.get('/api/post/10')
        self.assertEqual(response.status_code, 404)