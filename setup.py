from setuptools import setup, find_packages
import os

version = '1.0.3'
desc = "Infrastructure for maintaining a registry of available behaviors"
doc_files = [
    "README.rst",
    os.path.join("plone", "behavior", "behaviors.txt"),
    os.path.join("plone", "behavior", "directives.txt"),
    os.path.join("plone", "behavior", "annotation.txt"),
    os.path.join("docs", "CHANGES.rst"),
]
longdesc = '\n'.join([open(_).read() for _ in doc_files])


setup(
    name='plone.behavior',
    version=version,
    description=desc,
    long_description=longdesc,
    # more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
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
    extras_require={
        'test': [],
    },
    entry_points="""
    """,
)
