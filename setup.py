#!/usr/bin/env python

from distutils.core import setup

setup(name='nct-backend',
      version='0.1',
      description='NCTS backend',
      author='cn',
      author_email='lolexplode@gmail.com',
      packages=['nct'],
      install_requires=['sqlalchemy', 'psycopg2', 'passlib', 'flask', 'flask-sqlalchemy', 'flask-login']
     )
