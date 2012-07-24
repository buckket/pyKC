#!/usr/bin/python

from krautchan import Krautchan

kc = Krautchan(username='', password='', ssl=False)

mod = kc.get_mod()
print("%s (%s) ist Mod auf:" % (mod.username, mod.email))
for board in mod.boards:
    if not board['colleagues']:
        print("* %s (Alleiniger Moderator)" % (board['board']))
    else:
        print("* %s (Kollegen sind: %s)" % (board['board'], ', '.join(board['colleagues'])))

print kc.search_file(file='loom')
