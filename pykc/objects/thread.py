import json


class Thread(object):

    def __init__(self, id, board, flags, posts):
        self.id = id
        self.board = board
        self.flags = flags
        self.posts = posts

    def to_json(self):
        posts = []
        for post in self.posts:
            post_dict = post.to_safe_dict()
            posts.append(post_dict)
        thread = self.__dict__.copy()
        thread['posts'] = posts
        return json.dumps(thread)
