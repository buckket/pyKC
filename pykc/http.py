import requests

from .exceptions import LoginError


class HTTP(object):

    def __init__(self, username, password, timeout):
        self.base_url = "https://krautchan.net"

        self.username = username
        self.password = password
        self.timeout = timeout

        self.is_logged_in = False

        self.__session = requests.session()
        if username and password:
            self.__login()

    def __login(self):
        payload = {'username': self.username, 'password': self.password}
        result = self.__execute_request(self.base_url + '/ajax/login', params=payload)
        json = result.json()
        if json['success'] == 1:
            self.is_logged_in = True
        else:
            raise LoginError(json['messages'][0][1])

    def __execute_request(self, url=None, params=None):
            return self.__session.get(url, params=params, timeout=self.timeout)

    def get_search_file(self, name=None, strict=False):
        if strict:
            payload = {'name': name, 'mode': 'exact'}
        else:
            payload = {'name': name}
        return self.__execute_request(self.base_url + '/ajax/search/file', params=payload)

    def get_mod_info(self):
        return self.__execute_request(self.base_url + '/login')

    def get_thread(self, board=None, post=None):
        return self.__execute_request(self.base_url + '/resolve/' + str(board) + '/' + str(post))

    def get_file(self, url=None):
        return self.__execute_request(self.base_url + str(url))
