from krautchan.http import HTTP
from krautchan.parser import Parser

from operator import attrgetter


class Krautchan(object):

    def __init__(self, username=None, password=None, ssl=False):
        self.__http = HTTP(username=username, password=password, ssl=ssl)
        self.__parser = Parser()

    def get_modinfo(self):
        """Parse information available on the mod page and return a Mod object."""
        if self.__http.loggedIn is False:
            print("Ohne Anmeldung keine Nutzerinformationen")
            return None
        else:
            data = self.__http.get_modinfo()
            return self.__parser.parse_modinfo(data.text)

    def get_thread(self, board=None, post=None):
        """Parse a thread and return a Thread object."""
        data = self.__http.get_thread(board, post)
        return self.__parser.parse_thread(board, data.text)

    def get_post(self, board=None, post=None):
        """Parse the hole thread and return a single post as Post object, for now."""
        data = self.get_thread(board=board, post=post)
        return data.posts[map(attrgetter('id'), data.posts).index(post)]

    def search_file(self, name=None, beStrict=False):
        """Search for a file using KC AJAX API"""
        data = self.__http.get_search_file(name=name, beStrict=beStrict)
        return self.__parser.parse_search_file(data.json)
