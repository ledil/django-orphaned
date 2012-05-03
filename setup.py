#!/usr/bin/env python
from setuptools import setup

setup(
    name='django-orphaned',
    description='delete all orphaned files from your models',
    version='0.1',
    author='Leonardo Di Lella',
    author_email='leonardo.dilella@mobileapart.com',
    license='MIT',
    url='https://github.com/ledil/django-orphaned',
    packages=[
        'django_orphaned',
        'django_orphaned.management',
        'django_orphaned.management.commands'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: System :: Installation/Setup'
    ]
)
