from bs4 import BeautifulSoup
import requests

from krautchan.http import HTTP
from krautchan.parser import Parser
from krautchan.mod import Mod


class Krautchan(object):

	def __init__(self, username=None, password=None, ssl=False):
		self.__http = HTTP(username=username, password=password, ssl=ssl)
		self.__parser = Parser()

	def getMod(self):
		if self.__http.loggedIn is False:
			print "Ohne Anmeldung keine Nutzerinformationen"
		else:
			data = self.__http.getMod()
			result = self.__parser.parseMod(data.text)
			return Mod(result)
