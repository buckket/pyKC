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

    zip_safe=False,
    include_package_data=True,
    platforms='any',

    install_requires=[
        'BeautifulSoup4>=4.3.2',
        'requests>=2.4.1',
        'lxml>=3.4.0',
        'enum34>=1.0'
    ],

    description='Feed your snake with your favourite imageboard.',
    long_description=open('./README.rst', 'r').read(),
    keywords='imageboard, kc, parser',

    license='WTFPL',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)