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
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Chemistry',
        ],
      )
