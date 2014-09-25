import pprint

from pykc import Krautchan


kc = Krautchan()

print("\033[1mSearching for files:\033[0;0m")
pprint.pprint(kc.search_file(name='rfk'), width=100)

print("\n\033[1mParsing given thread.\033[0;0m")
thread = kc.get_thread('prog', '1698')

print("\n\033[1mShowing thread class:\033[0;0m")
pprint.pprint(thread.__dict__)

print("\n\033[1mShowing posts in Thread:\033[0;0m")
for post in thread.posts:
    pprint.pprint(post.__dict__)

print("\n\033[1mJSON representation:\033[0;0m")
print(thread.to_json())

print("\n\033[1mNewest post id on b:\033[0;0m")
print(kc.get_newest_post_id('b'))
