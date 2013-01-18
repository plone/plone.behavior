from setuptools import setup, find_packages
import os

version = '1.0.2'

setup(name='plone.behavior',
      version=version,
      description="Infrastructure for maintaining a registry of available behaviors",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("plone", "behavior", "behaviors.txt")).read() + "\n" +
                       open(os.path.join("plone", "behavior", "directives.txt")).read() + "\n" +
                       open(os.path.join("plone", "behavior", "annotation.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        ],
      keywords='Plone behavior registry',
      author='Martin Aspeli',
      author_email='optilude@gmail.com',
      url='http://code.google.com/p/dexterity',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.interface',
          'zope.schema',
          'zope.annotation',
          'zope.configuration',
      ],
      extras_require = {
          'test': [],
      },
      entry_points="""
      """,
      )
