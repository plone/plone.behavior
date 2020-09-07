from setuptools import find_packages
from setuptools import setup


version = '1.4.0'
desc = "Infrastructure for maintaining a registry of available behaviors"
doc_files = [
    "README.rst",
    "CHANGES.rst",
]
longdesc = '\n'.join([open(_).read() for _ in doc_files])


setup(
    name='plone.behavior',
    version=version,
    description=desc,
    long_description=longdesc,
    # more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 6 - Mature",
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='Plone behavior registry',
    author='Martin Aspeli',
    author_email='optilude@gmail.com',
    url='https://pypi.org/project/plone.behavior',
    license='BSD',
    packages=find_packages(),
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.configuration',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'zope.lifecycleevent',
        ],
    },
    entry_points="""
    """,
)
