pyKC
####

Feed your snake with your favourite imageboard.


| **In other words:**
| This Python library provides high-level access to a KC thread and/or post (including all available metadata) by parsing the HTML source, additionally various endpoints of the KC AJAX API can be called.

Minimal Requirements:
---------------------

**Core:**

- Python >= 2.6

**Modules:**

- `lxml <http://lxml.de/>`_
- `enum34 <https://pypi.python.org/pypi/enum34>`_
- `requests <http://docs.python-requests.org/en/latest/index.html>`_
- `BeautifulSoup4 <http://www.crummy.com/software/BeautifulSoup/>`_

Features
--------
- Check ``pykc/core.py`` and ``pykc.py`` or the example code below. :-)

.. code:: python

    from pykc import Krautchan


    kc = Krautchan()

    print(kc.search_file(name='rfk'))

    thread = kc.get_thread('prog', '1698')
    print(thread.__dict__)
    print(thread.to_json())

    print kc.get_newest_post_id('b')


Credits
-------
**Main author:** buckket

License
-------

::

        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2004 Sam Hocevar <sam@hocevar.net>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
