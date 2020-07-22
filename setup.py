# !/usr/bin/env python
# from distutils.core import setup
from io import open

from setuptools import setup


def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


setup(
  name='keyboa',
  packages=['keyboa'],
  version='2.2.4',
  license='MIT',
  description="Telegram Inline Keyboards Generator",
  long_description=read("README.md"),
  long_description_content_type="text/markdown",
  author='torrua',
  author_email='torrua@gmail.com',
  url='https://github.com/torrua/keyboa',
  download_url='https://github.com/torrua/keyboa/archive/v2.2.4.tar.gz',
  keywords=['Generate', 'Inline', 'Keyboard', 'Telegram'],
  install_requires=[
          'pytelegrambotapi',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',  # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
