import json
import pickle


class Thread(object):

    def __init__(self, id, board, flags, posts):
        self.id = id
        self.board = board
        self.flags = flags
        self.posts = posts

    def to_safe_dict(self):
        posts = []
        for post in self.posts:
            post_dict = post.to_safe_dict()
            posts.append(post_dict)
        thread = self.__dict__.copy()
        thread['posts'] = posts
        return thread

    def to_json(self):
        return json.dumps(self.to_safe_dict())

    def to_pickle(self):
        return pickle.dumps(self.to_safe_dict())
