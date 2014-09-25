import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')


with open('pykc/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(
    name='pykc',
    version=version,

    url='http://github.com/buckket/pykc',

    author='buckket',

    packages=['pykc', 'pykc.objects'],

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