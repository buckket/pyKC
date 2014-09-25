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

    def __execute_request(self, url, params=None):
        return self.__session.get(url, params=params, timeout=self.timeout)

    def __login(self):
        payload = {'username': self.username, 'password': self.password}
        result = self.__execute_request('{}/ajax/login'.format(self.base_url), params=payload)
        json = result.json()
        if json['success'] == 1:
            self.is_logged_in = True
        else:
            raise LoginError(json['messages'][0][1])

    def get_search_file(self, name, strict=False):
        if strict:
            payload = {'name': name, 'mode': 'exact'}
        else:
            payload = {'name': name}
        return self.__execute_request('{}/ajax/search/file'.format(self.base_url), params=payload)

    def get_mod_info(self):
        return self.__execute_request('{}/login'.format(self.base_url))

    def get_thread(self, board, post):
        return self.__execute_request('{}/resolve/{}/{}'.format(self.base_url, board, post))

    def get_overview(self, board):
        return self.__execute_request('{}/{}/'.format(self.base_url, board))

    def get_file(self, url):
        return self.__execute_request('{}{}'.format(self.base_url, url))
