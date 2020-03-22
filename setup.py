from __future__ import absolute_import
from __future__ import unicode_literals

import glob
import os

from setuptools import setup, find_packages


def find(filename):
    return glob.glob(filename)


def read_file(filename):
    basepath = os.path.dirname(os.path.dirname(__file__))
    filepath = os.path.join(basepath, filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


LONG_DESC = ''
try:
    import pypandoc

    LONG_DESC = pypandoc.convert('README.md', 'rst', format='markdown_github')
except (IOError, ImportError):
    LONG_DESC = read_file('README.md')


def _requires_from_file(filename):
    return open(filename).read().splitlines()


cszp_files = ["cszp/index.html", "cszp/nofile.png", "cszp/version"]
cszp_files += find("cszp/*.json")
setup(
    name="cszp",
    version=open("cszp/version").read().splitlines()[0],
    url='https://github.com/kumitatepazuru/cszp',
    author='kumitatepazuru',
    author_email='teltelboya18@gmail.com',
    maintainer='kumitatepazuru',
    maintainer_email='teltelboya18@gmail.com',
    description='cszp Easy soccer execution program',
    long_description=readme,
    packages=find_packages(),
    install_requires=[
        "numpy",
        "texttable",
        "matplotlib",
        "tqdm",
        "pandas",
        "urllib3",
        "cuitools"
    ],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      cszp = cszp.__init__:main
    """,
    data_files=[("/cszp", cszp_files), ("/cszp/language", find("cszp/language/*.lang"))]
)
