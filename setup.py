from __future__ import absolute_import
from __future__ import unicode_literals

import glob

from setuptools import setup, find_packages


def find(filename):
    return list(map(lambda n: n[5:], glob.glob(filename)))


# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


cszp_files = ["html/index.html", "html/nofile.png", "html/load.gif", "version"] + find("cszp/language/*.lang")
cszp_files += find("cszp/*.json") + find("cszp/language/*.json")
# print(find("cszp/language/*.lang"))
setup(
    name="cszp",
    version=open("cszp/version").read().splitlines()[0],
    url='https://github.com/kumitatepazuru/cszp',
    author='kumitatepazuru',
    author_email='teltelboya18@gmail.com',
    maintainer='kumitatepazuru',
    maintainer_email='teltelboya18@gmail.com',
    description='cszp Easy soccer execution program',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "texttable",
        "matplotlib",
        "pandas",
        "urllib3",
        "cuitools==1.7.0.2",
        "prompt-toolkit",
        "dateutils"
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
    package_data={"cszp": cszp_files}
)
