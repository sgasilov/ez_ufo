# setup.py
from setuptools import setup

setup(name='ez_ufo',
    version='1.0',
    description='GUI for making ufo-kit data processing pipelines',
    author='Sergei Gasilov',
    url='https://bmit.lightsource.ca',
    packages=['ez_ufo'],
    package_data={'ez_ufo': ['block_diagram.jpg']},
    scripts=['bin/ezufo', 'bin/eznlmdn']
    )

