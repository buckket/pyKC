# -*- coding: utf-8 -*-
"""
    pyKC
    ~~~~

    Parse your favorite imageboard using Python.

    :copyright: (c) 2014 by buckket.
    :license: WTFPL, see LICENSE for more details.
"""

# Core classes
from .core import Krautchan

# Types
from .objects import UserClass

# Exceptions
from .exceptions import UsageError, LoginError, ThreadNotFound, KCError


__all__ = [
    # Core classes
    'Krautchan',

    # Types
    'UserClass',

    # Exceptions
    'UsageError', 'LoginError', 'ThreadNotFound', 'KCError',
]


__version__ = '1.0-dev'
