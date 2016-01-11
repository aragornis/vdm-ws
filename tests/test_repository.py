import unittest
from datetime import datetime
from posts.repository import Posts
from posts.repository import Post

post1 = Post(0, 1, datetime(2015, 5, 5))
post2 = Post(2, 1, datetime(2015, 11, 2))

class PostsTests(unittest.TestCase):
    def setUp(self):
        # Open non-persisted db
        self.__repository = Posts(':memory:', True)
        self.__repository.addPost(post1)
        self.__repository.addPost(post2)

    def test_addPost(self):
        self.__repository.addPost(Post(3, 3, datetime(2016, 11, 2)))
        self.assertEqual(self.__repository.getPostsCount(), 3)

    def test_getPost(self):
        self.assertPostEqual(self.__repository.getPost(0), post1)
        self.assertPostEqual(self.__repository.getPost(1), post2)
        self.assertEqual(self.__repository.getPost(5), None) # Non-existing post id returns None

    def test_getPosts_no_query(self):
        posts = self.__repository.getPosts()
        self.assertEqual(len(posts), 2)
        self.assertPostEqual(posts[0], post1)
        self.assertPostEqual(posts[1], post2)

    def test_getPosts_by_author(self):
        posts = self.__repository.getPosts(None, None, 2)
        self.assertEqual(len(posts), 1)
        self.assertPostEqual(posts[0], post2)

    def test_getPosts_by_date(self):
        posts = self.__repository.getPosts(datetime(2015, 10, 2), datetime(2016, 5, 5))
        self.assertEqual(len(posts), 1)
        self.assertPostEqual(posts[0], post2)

    def test_getPosts_by_all(self):
        posts = self.__repository.getPosts(datetime(2015, 10, 2), datetime(2016, 5, 5), 0)
        self.assertEqual(len(posts), 0)

    def assertPostEqual(self, p1, p2):
        self.assertEqual(p1.toDisplayableDict(), p2.toDisplayableDict())