import requests


class HTTP(object):

	def __init__(self, username=None, password=None, ssl=False):
		pass

		self.username = username
		self.password = password
		self.loggedIn = False
		self.ssl = ssl

		if ssl == True:
			self.baseURL = 'https://krautchan.net'
		else:
			self.baseURL = 'http://krautchan.net'

		if username and password != None:
			self.__session = requests.session(verify=False)
			self.__login()
		else:
			self.__session = requests.session(verify=False)

	def __login(self):
		payload = {'username':self.username, 'password':self.password}
		result = self.__session.get(self.baseURL + '/ajax/login', params=payload)
		json = result.json
		if json['success'] == 1:
			self.loggedIn = True
			print "Erfolgreich angemeldet."
		else:
			for error in json['messages']:
				print 'Fehler: ' + error[1]
				raise SystemExit()

	def getMod(self):
		return self.__session.get(self.baseURL + '/login')
