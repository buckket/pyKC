import re
from bs4 import BeautifulSoup

from krautchan.objects.mod import Mod


class Parser(object):

	def parseMod(self, input):
		soup = BeautifulSoup(input)

		username = soup.find(text=re.compile("Angemeldet als")).next_sibling.text
		email = soup.find(name='input', id='email')['value']

		boards = []
		for element in soup.find(text=re.compile('Team')).next_element.next_element.find_all('b'):
			if element.text[0] == '/':
				boards.append({'board':element.text, 'colleagues': []})
			else:
				boards[-1]['colleagues'].append(element.text)

		return Mod(username=username, email=email, boards=boards)
