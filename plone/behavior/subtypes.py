from zope.interface import alsoProvides
from plone.behavior.interfaces import IBehaviorAssignable

def apply_subtypes(obj, event):
    """Event handler to apply subtypes for all behaviors enabled
    for the given type.
    """
    
    assignable = IBehaviorAssignable(obj, None)
    if assignable is None:
        return
        
    for behavior in assignable.enumerate_behaviors():
        if behavior.subtype is not None:
            alsoProvides(obj, behavior.subtype)