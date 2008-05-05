from zope.interface import implements
from zope.component import getUtility

from zope.app.interface import queryType
from zope.app.content.interfaces import IContentType

from plone.behavior.interfaces import IBehaviorAssignable
from plone.behavior.interfaces import IBehaviorRegistry

class ContentTypeBehaviorAssignable(object):
    """Sample adapter that uses queryType for a given interface (IContentType
    by default) to determine the type of its context, and then looks up a
    IBehaviorRegistry utility to determine whether behaviors are registered
    for that context type.
    """
    
    implements(IBehaviorAssignable)
    # adapts(Interface)  --> leave this up to the application
    
    _type_interface = IContentType
    
    def __init__(self, context):
        self.context = context
        self.type = queryType(context, self._type_interface)
        self.registry = getUtility(IBehaviorRegistry)
        
    def supports(self, behavior_interface):
        return self.registry.is_registered(self.type, behavior_interface)
        
    def enumerate_behaviors(self):
        return self.registry.enumerate(self.type)