import unittest

import zope.testing.doctest
import zope.component.testing
import zope.app.testing.placelesssetup

import plone.behavior.registry

# Dummy behavior for the directives.txt test
from zope.interface import Interface, implements

class IDummyBehavior(Interface):
    pass
    
class DummyBehavior(object):
    implements(IDummyBehavior)
    def __init__(self, context):
        self.context = context

def test_suite():
    return unittest.TestSuite((
        
        zope.testing.doctest.DocFileSuite('behaviors.txt',
                     # setUp=setUp,
                     tearDown=zope.component.testing.tearDown),
        
        zope.testing.doctest.DocFileSuite('directives.txt',
                     setUp=zope.app.testing.placelesssetup.setUp,
                     tearDown=zope.app.testing.placelesssetup.tearDown),
                     
        zope.testing.doctest.DocTestSuite(plone.behavior.registry,
                     # setUp=setUp,
                     tearDown=zope.app.testing.placelesssetup.tearDown),
                     
        ))