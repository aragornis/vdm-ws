from pydblite import Base
from datetime import datetime
import json

class Post:
    def __init__(self, author, content, date, id = None):
        self.id = id
        self.author = author
        self.content = content
        self.date = date

    def toDisplayableDict(self):
        dic = dict(self.__dict__)
        dic['date'] = dic['date'].strftime('%Y-%m-%d %H:%M:%S')
        return dic

class Posts:
    def __init__(self, filename, erase_db):
        self.db = Base(filename)
        self.db.create('author', 'content', 'date', mode="override" if erase_db else "open")

    def addPost(self, post):
        post.id = self.db.insert(author = post.author, content = post.content, date = post.date)
        self.db.commit()

    def getPost(self, id):
        db_entry = self.db[id]
        return self.__createPost(db_entry) if db_entry is not None else None

    def getPosts(self, from_date, to_date, author):
        iterator = self.db
        if from_date is not None:
            iterator = iterator and (self.db("date") >= from_date)
        if to_date is not None:
            iterator = iterator and (self.db("date") <= to_date)
        if author is not None:
            iterator = iterator and (self.db("author") == author)

        return [self.__createPost(db_entry) for db_entry in iterator]

    def getPostsCount(self):
        return len(self.db)

    def __createPost(self, db_entry):
        return Post(db_entry['author'], db_entry['content'], db_entry['date'], db_entry['__id__'])