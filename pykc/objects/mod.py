import json


class Mod(object):

    def __init__(self, username=None, email=None, boards=None):
        self.username = username
        self.email = email
        self.boards = boards

    def to_json(self):
        return json.dumps(self.__dict__)
