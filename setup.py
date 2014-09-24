from setuptools import setup

from pykc import __version__


setup(
    name='pykc',
    version=__version__,

    url='http://github.com/buckket/pykc',

    author='buckket',

    packages=['pykc'],

    zip_safe=True,
    include_package_data=True,

    install_requires=['BeautifulSoup4', 'requests', 'lxml', 'enum34'],

    description='Parse your favorite imageboard using Python.',
    long_description=open('./README.md', 'r').read(),
    keywords='imageboard, kc',

    license='WTFPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'License :: Public Domain',
    ],
)