import re
from bs4 import BeautifulSoup

from krautchan.objects.mod import Mod
from krautchan.objects.post import Post
from krautchan.objects.thread import Thread


class Parser(object):

    def parse_modinfo(self, input):
        soup = BeautifulSoup(input)

        username = soup.find(text=re.compile('Angemeldet als')).next_sibling.text
        email = soup.find(name='input', id='email')['value']

        boards = []
        for element in soup.find(text=re.compile('Team')).next_element.next_element.find_all('b'):
            if element.text[0] == '/':
                boards.append({'board': element.text, 'colleagues': []})
            else:
                boards[-1]['colleagues'].append(element.text)

        return Mod(username=username, email=email, boards=boards)

    def parse_search_file(self, input):
        return input['data']['files']

    def parse_thread(self, board, input):
        soup = BeautifulSoup(input)

        if soup.select('.message_text'):
            if re.search('existiert nicht|does not exist', soup.select('.message_text')[0].text):
                raise SystemExit('Thread existiert nicht mehr')

        thread = {}
        # Parse the thread flags (sticky, locked, and so on)
        thread['flags'] = {}
        thread['flags']['sticky'] = True if soup.select('img[src^="/images/sticky"]') else False
        thread['flags']['locked'] = True if soup.select('img[src^="/images/locked"]') else False

        thread['board'] = board

        op = {}
        # Parse the original post.
        op['id'] = soup.select('.quotelink')[1].text
        op['subject'] = soup.select('.postsubject')[0].text
        op['name'] = soup.select('.postername')[0].text
        op['date'] = soup.select('.postdate')[0].text
        op['text'] = soup.select('#post_text_' + op['id'])[0].text

        thread['id'] = op['id']

        op['tripcode'] = soup.select('.postheader')[0].select('.tripcode')[0].text if \
            soup.select('.postheader')[0].select('.tripcode') else None
        op['cb'] = soup.select('.postheader')[0].select('img[src^="/images/balls/]')[0].get('src') if \
            soup.select('.postheader')[0].select('img[src^="/images/balls/]') else None

        op['sage'] = True if soup.select('.postheader')[0].select('.sage') else False

        # Parse mod information if available.
        if soup.select('#posterinfo_' + op['id']):
            op['posterinfo'] = self._extract_posterinfo(soup, op['id'])
        else:
            op['posterinfo'] = None


        if soup.select('.postheader')[0].select('.authority_mod'):
            op['level'] = 'mod'
        elif soup.select('.postheader')[0].select('.authority_admin'):
            op['level'] = 'admin'
        else:
            op['level'] = 'user'

        op['files'] = []
        for fileSection in soup.select('.file_thread'):
            file = {}
            file['name'] = fileSection.next_element.next_element.text
            file['download'] = fileSection.select('a[href^="/download/"]')[0].get('href')
            file['thumbnail'] = fileSection.select('img[src^="/thumbnails/"]')[0].get('src')
            op['files'].append(file)

        thread['posts'] = []
        thread['posts'].append(Post(**op))

        # Parse the replies.
        for replySection in soup.select('.postreply'):
            reply = {}
            reply['id'] = replySection.select('.quotelink')[1].text
            reply['subject'] = replySection.select('.postsubject')[0].text
            reply['name'] = replySection.select('.postername')[0].text
            reply['date'] = replySection.select('.postdate')[0].text
            reply['text'] = replySection.select('#post_text_' + reply['id'])[0].text

            reply['tripcode'] =replySection.select('.tripcode')[0].text if \
                replySection.select('.tripcode') else None
            reply['cb'] = replySection.select('img[src^="/images/balls/]')[0].get('src') if \
                replySection.select('img[src^="/images/balls/]') else None

            reply['sage'] = True if replySection.select('.sage') else False

            # Parse mod information if available.
            if soup.select('#posterinfo_' + reply['id']):
                reply['posterinfo'] = self._extract_posterinfo(soup, reply['id'])
            else:
                reply['posterinfo'] = None

            if replySection.select('.authority_mod'):
                reply['level'] = 'mod'
            elif replySection.select('.authority_admin'):
                reply['level'] = 'admin'
            else:
                reply['level'] = 'user'

            reply['files'] = []
            for fileSection in replySection.select('.file_reply'):
                file = {}
                file['name'] = fileSection.next_element.next_element.text
                file['download'] = fileSection.select('a[href^="/download/"]')[0].get('href')
                file['thumbnail'] = fileSection.select('img[src^="/thumbnails/"]')[0].get('src')
                reply['files'].append(file)

            thread['posts'].append(Post(**reply))

        return Thread(**thread)

    def _extract_posterinfo(self, soup, id):
        info = {}
        posterinfo = soup.select('#posterinfo_' + id)[0]
        info['ip'] = re.search(
            re.compile("((?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))(?:\.(?:\d|[1-9]\d|1\d\d|2(?:[0-4]\d|5[0-5]))){3})"),
            posterinfo.text
            ).group(0)
        info['hostname'] = posterinfo.select('i')[0].text[1:-1]
        info['location'] = posterinfo.select('img')[0].next_element[8:-1]
        return info
