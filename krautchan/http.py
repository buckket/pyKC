import requests


class HTTP(object):

    def __init__(self, username=None, password=None, ssl=False):
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
        result = self.__execute_request(self.baseURL + '/ajax/login', params=payload)
        json = result.json
        if json['success'] == 1:
            self.loggedIn = True
            print("Erfolgreich angemeldet.")
        else:
            for error in json['messages']:
                print('Fehler: ' + error[1])
                raise SystemExit()

    def __execute_request(self, url=None, params=None):
            return self.__session.get(url, params=params, timeout=5.0)

    def get_search_file(self, file=None, beStrict=False):
        if beStrict:
            payload = {'name':file, 'mode':'exact'}
        else:
            payload = {'name':file}
        return self.__execute_request(self.baseURL + '/ajax/search/file', params=payload)

    def get_mod(self):
        return self.__execute_request(self.baseURL + '/login')

    def get_thread(self, board=None, post=None):
        return self.__execute_request(self.baseURL + '/resolve/' + board + '/' + post)
