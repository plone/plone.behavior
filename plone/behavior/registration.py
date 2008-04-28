from zope.interface import implements

from plone.behavior.interfaces import IBehavior

class BehaviorRegistration(object):
    implements(IBehavior)
    
    def __init__(self, title, description, interface, factory):
        self.title = title
        self.description = description
        self.interface = interface
        self.factory = factory