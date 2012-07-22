from krautchan.http import HTTP
from krautchan.parser import Parser


class Krautchan(object):

	def __init__(self, username=None, password=None, ssl=False):
		self.__http = HTTP(username=username, password=password, ssl=ssl)
		self.__parser = Parser()

	def getMod(self):
		if self.__http.loggedIn is False:
			print "Ohne Anmeldung keine Nutzerinformationen"
		else:
			data = self.__http.getMod()
			return self.__parser.parseMod(data.text)
