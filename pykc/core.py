from operator import attrgetter

from .http import HTTP
from .parser import Parser
from .exceptions import UsageError


class Krautchan(object):
    """This object represents the core interface to interact with Krautchan.

    Access to some mod/admin specific functions is only available if you provide a valid username and password.
    If so, you will be automatically logged in. Otherwise a call of those functions will result in a `UsageError`.

    :param username: the username of your KC account.
    :param password: the password of your KC account.
    :param timeout: the timeout value for HTTP requests.
    :param try_poster_info: try to extract poster information (requires mod status).
    """

    def __init__(self, username=None, password=None, timeout=20.0, try_poster_info=False):
        self.__http = HTTP(username=username, password=password, timeout=timeout)
        self.__parser = Parser()

        self.try_poster_info = try_poster_info

    def get_mod_info(self):
        """Parse the information available on the mod page and return a Mod object.
        Warning: only available if you're logged in!
        """
        if self.__http.is_logged_in is False:
            raise UsageError('You have to be logged in to use this function.')
        else:
            data = self.__http.get_mod_info()
            return self.__parser.parse_mod_info(data.text)

    def get_thread(self, board, post):
        """Parse a thread and return a Thread object.

        :param board: the board.
        :param post: the id of a post or the thread id.
        """
        data = self.__http.get_thread(board=board, post=post)
        return self.__parser.parse_thread(board=board, data=data, try_poster_info=self.try_poster_info)

    def get_post(self, board, post):
        """Parse the hole thread and return a single post as Post object, for now.

        :param board: the board.
        :param post: the id of a specific post.
        """
        data = self.get_thread(board=board, post=post)
        return data.posts[map(attrgetter('id'), data.posts).index(post)]

    def get_file(self, url):
        """Return the requested file from KC.
        The base path will be added automatically.

        :param url: url to fetch.
        """
        data = self.__http.get_file(url=url)
        return data.content

    def search_file(self, name, strict=False):
        """Search for a file using the private KC AJAX API.

        :param name: the file name to search.
        :param strict: if set to `True` search will only include exact matches.
        """
        data = self.__http.get_search_file(name=name, strict=strict)
        return self.__parser.parse_search_file(data.json())
