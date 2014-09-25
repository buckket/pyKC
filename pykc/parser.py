import re
import time

from bs4 import BeautifulSoup

from .objects import UserClass
from .objects.mod import Mod
from .objects.post import Post
from .objects.thread import Thread
from .exceptions import ThreadNotFound


class Parser(object):

    @staticmethod
    def parse_mod_info(data):
        soup = BeautifulSoup(data)

        username = soup.find(text=re.compile('Angemeldet als')).next_sibling.text
        email = soup.find(name='input', id='email')['value']

        boards = []
        for element in soup.find(text=re.compile('Team')).next_element.next_element.find_all('b'):
            if element.text[0] == '/':
                boards.append({'board': element.text, 'colleagues': []})
            else:
                boards[-1]['colleagues'].append(element.text)

        return Mod(username=username, email=email, boards=boards)

    @staticmethod
    def parse_search_file(data):
        return data['data']['files']

    @staticmethod
    def parse_thread(board, data, try_poster_info):
        timer_start = time.clock()
        soup = BeautifulSoup(data.text, 'lxml')

        message_text = soup.find_all('td', {'class': 'message_text'}, limit=1)
        if message_text:
            if re.search('existiert nicht|does not exist', message_text[0].text):
                raise ThreadNotFound()

        # Creating a thread dict.
        thread = {'board': board}

        # Parse the thread flags (sticky, locked, and so on).
        post_header = soup.find_all('div', {'class': 'postheader'}, limit=1)[0]
        thread['flags'] = {'sticky': True if post_header.select('img[src^="/images/sticky"]') else False,
                           'locked': True if post_header.select('img[src^="/images/locked"]') else False}

        # Parse the original post.
        op = {}
        op['id'] = int(soup.find_all('a', {'class': 'quotelink'}, limit=2)[1].text)

        subject = soup.find_all('span', {'class': 'postsubject'}, limit=1)[0].text
        op['subject'] = subject if subject else None

        op['name'] = soup.find_all('span', {'class': 'postername'}, limit=1)[0].text
        op['date'] = soup.find_all('span', {'class': 'postdate'}, limit=1)[0].text
        op['text'] = soup.select('#post_text_' + str(op['id']))[0].text

        op['tripcode'] = post_header.select('.tripcode')[0].text if \
            post_header.select('.tripcode') else None
        op['cb'] = post_header.select('img[src^="/images/balls/]')[0].get('src') if \
            post_header.select('img[src^="/images/balls/]') else None

        op['sage'] = True if post_header.select('.sage') else False

        post_body = soup.find_all('div', {'class': 'postbody'}, limit=1)[0]
        op['ban'] = True if post_body.select('.ban_mark') else False

        # Parse mod information if enabled and available.
        if try_poster_info and soup.select('#posterinfo_' + op['id']):
            op['posterinfo'] = extract_posterinfo(soup, op['id'])
        else:
            op['posterinfo'] = None

        # Parse user class.
        if post_header.select('.authority_mod'):
            op['level'] = UserClass.mod
        elif post_header.select('.authority_admin'):
            op['level'] = UserClass.admin
        else:
            op['level'] = UserClass.user

        # Extract files.
        op['files'] = extract_files(soup.select('.file_thread'))

        thread['posts'] = []
        thread['posts'].append(Post(**op))
        thread['id'] = op['id']

        # Parse the replies.
        for reply_section in soup.select('.postreply'):
            reply = {}
            reply['id'] = int(reply_section.select('.quotelink')[1].text)

            subject = reply_section.select('.postsubject')[0].text
            reply['subject'] = subject if subject else None

            reply['name'] = reply_section.select('.postername')[0].text
            reply['date'] = reply_section.select('.postdate')[0].text
            reply['text'] = reply_section.select('#post_text_' + str(reply['id']))[0].text

            reply['tripcode'] = reply_section.select('.tripcode')[0].text if \
                reply_section.select('.tripcode') else None
            reply['cb'] = reply_section.select('img[src^="/images/balls/]')[0].get('src') if \
                reply_section.select('img[src^="/images/balls/]') else None

            reply['sage'] = True if reply_section.select('.sage') else False
            reply['ban'] = True if reply_section.select('.ban_mark') else False

            # Parse mod information if available.
            if try_poster_info and soup.select('#posterinfo_' + reply['id']):
                reply['posterinfo'] = extract_posterinfo(soup, reply['id'])
            else:
                reply['posterinfo'] = None

            # Parse user class.
            if reply_section.select('.authority_mod'):
                reply['level'] = UserClass.mod
            elif reply_section.select('.authority_admin'):
                reply['level'] = UserClass.admin
            else:
                reply['level'] = UserClass.user

            # Extract files.
            reply['files'] = extract_files(reply_section.select('.file_reply'))

            thread['posts'].append(Post(**reply))

        timer_end = time.clock()
        print("Finished in %.2gs." % (timer_end - timer_start))
        return Thread(**thread)

    @staticmethod
    def parse_newest_post_id(data):
        soup = BeautifulSoup(data.text, 'lxml')
        thread = soup.find_all('div', {'class': 'thread'}, limit=1)[0]
        posts = thread.find_all('a', {'class': 'quotelink'})
        return int(posts[-1].text.strip())


def extract_posterinfo(soup, post_id):
    info = {}
    posterinfo = soup.select('#posterinfo_' + post_id)[0]
    info['ip'] = re.search(
        re.compile("((?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))(?:\.(?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))){3})"),
        posterinfo.text
    ).group(0)
    info['hostname'] = posterinfo.select('i')[0].text[1:-1]
    info['location'] = posterinfo.select('img')[0].next_element[8:-1]
    return info


def extract_files(data):
    files = []
    for file_section in data:
        file_dict = {}
        file_dict['name'] = file_section.next_element.next_element.text
        file_dict['download'] = file_section.select('a[href^="/download/"]')[0].get('href')

        # Beware! Special case:
        # If you upload anything but an image or video the thumbnail will actually be an image
        # representing that specific media type. The URL will change from `/thumbnail/` to `/images/`.
        # Conclusion: If there's no `/thumbnail/` there must be `/images/`. Try to grab them.
        try:
            file_dict['thumbnail'] = file_section.select('img[src^="/thumbnails/"]')[0].get('src')
        except IndexError:
            file_dict['thumbnail'] = file_section.select('img[src^="/images/"]')[0].get('src')

        files.append(file_dict)
    return files
