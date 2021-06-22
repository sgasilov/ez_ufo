from setuptools import setup, find_packages

setup(name='ez_ufo_qt',
      version='0.5',
      description='GUI for making ufo-kit data processing pipelines',
      author='Sergei Gasilov',
      url='https://bmit.lightsource.ca',
      packages=find_packages(),
      include_package_data=True,
      package_data={'ez_ufo_qt': ['ez_ufo_qt/GUI/default_settings.yaml']},
      install_requires=[],
      scripts=['bin/ezufo'])