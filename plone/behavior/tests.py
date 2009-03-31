import unittest

import zope.testing.doctest
import zope.component.testing
import zope.app.testing.placelesssetup

# Dummy behaviors for the directives.txt test
from zope.interface import Interface, implements
from zope.component import adapts

# Simple behavior

class IDummyBehavior(Interface):
    pass

class DummyBehavior(object):
    implements(IDummyBehavior)
    def __init__(self, context):
        self.context = context

# Behavior with subtype

class IDummySubtypeBehavior(Interface):
    pass
    
class IDummySubtypeBehaviorMarker(Interface):
    pass

class IMinimalContextRequirements(Interface):
    pass

class DummySubtypeBehavior(object):
    implements(IDummySubtypeBehavior)
    def __init__(self, context):
        self.context = context

# Behavior with subtype and no factory

class ISubtypeOnlyMarker(Interface):
    pass

# Behavior with interface and for_ implied by factory

class IDummyImpliedBehavior(Interface):
    pass

class ISomeContext(Interface):
    pass

class DummyImpliedBehavior(object):
    implements(IDummyBehavior)
    adapts(ISomeContext)
    
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