from krautchan.http import HTTP
from krautchan.parser import Parser


class Krautchan(object):

    def __init__(self, username=None, password=None, ssl=False):
        self.__http = HTTP(username=username, password=password, ssl=ssl)
        self.__parser = Parser()

    def get_mod(self):
        if self.__http.loggedIn is False:
            print("Ohne Anmeldung keine Nutzerinformationen")
        else:
            data = self.__http.get_mod()
            return self.__parser.parse_mod(data.text)

    def search_file(self, file=None, beStrict=False):
        data = self.__http.get_search_file(file=file, beStrict=beStrict)
        return self.__parser.parse_search_file(data.json)
