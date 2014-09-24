import json
import pickle


class Mod(object):

    def __init__(self, username=None, email=None, boards=None):
        self.username = username
        self.email = email
        self.boards = boards

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_pickle(self):
        return pickle.dumps(self.__dict__)
