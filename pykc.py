#!/usr/bin/python

from krautchan import Krautchan

import pprint
import inspect

#kc = Krautchan(username='MrLoom', password='benisInVagina', ssl=False)
kc = Krautchan(ssl=False)

mod = kc.get_modinfo()
if mod:
    print("%s (%s) ist Mod auf:" % (mod.username, mod.email))
    for board in mod.boards:
        if not board['colleagues']:
            print("* %s (Alleiniger Moderator)" % (board['board']))
        else:
            print("* %s (Kollegen sind: %s)" % (board['board'], ', '.join(board['colleagues'])))

print("\n")

#pprint.pprint(kc.search_file(name='rfk'), width=100)

print("\033[1mParsing given thread.\033[0;0m")
thread = kc.get_thread('kc', '30685')
print("\033[1mShowing Thread class:\033[0;0m")
pprint.pprint(thread.__dict__)
print("\n\033[1mShowing Posts in Thread:\033[0;0m")
for post in thread.posts:
    pprint.pprint(post.__dict__)
    print("")

print("\n\033[1mTrying to get a specific post:\033[0;0m")
post = kc.get_post('kc', '30685')
pprint.pprint(post.__dict__)
