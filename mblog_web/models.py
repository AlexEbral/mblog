import time


class User:
    def __init__(self, name='', pwd=''):
        self.name = name
        self.pwd = pwd


class Post:
    def __init__(self, author='', subject='', body='', datetime=None, **kwargs):
        self.author = author
        self.subject = subject
        self.body = body
        self.datetime = int(time.time())*1000 if datetime is None else datetime


class Comment:
    def __init__(self, post_id='', author='', body='', datetime=None, **kwargs):
        self.post_id = post_id
        self.author = author
        self.body = body
        self.datetime = int(time.time())*1000 if datetime is None else datetime