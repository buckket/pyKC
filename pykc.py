#!/usr/bin/python

from krautchan import Krautchan

kc = Krautchan(username='', password='', ssl=True)
mod = kc.getMod()

print "%s (%s) ist Mod auf:" % (mod.username, mod.email)
for board in mod.boards:
	print "* %s (Kollegen sind: %s)"  % (board['board'], ', '.join(board['colleagues']))
