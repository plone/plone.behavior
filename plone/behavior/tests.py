import unittest

import zope.testing.doctest
import zope.component.testing
import zope.app.testing.placelesssetup

import plone.behavior.interfaces

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
        
        ))