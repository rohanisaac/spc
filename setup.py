#!/usr/bin/env python

from distutils.core import setup

import spc

setup(name='spc',
      version=spc.__version__,
      description=spc.__doc__,
      author=spc.__author__,
      author_email=spc.__author_email__,
      url='https://github.com/rohanisaac/spc',
      packages=['spc'],
      install_requires=['numpy'],
      )
