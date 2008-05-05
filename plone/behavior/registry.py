from persistent import Persistent
from BTrees.OOBTree import OOBTree, OOSet

from zope.interface import implements
from zope.component import getUtility

from plone.behavior.interfaces import IBehaviorRegistry, IBehavior

class PersistentBehaviorRegistry(Persistent):
    """A persistent registry that can be configured as a local utility.
    
    To test this, let's create a simple interface.
    
        >>> from zope.interface import Interface
        >>> class IOne(Interface): pass
        >>> class ITwo(Interface): pass
    
    We also need to register two named behaviors to test with. In this case,
    we won't actually bother with the behavior factory, since we're only
    interested in getting the interface back. For a more realistic example,
    see behaviors.txt.
    
        >>> class IBehaviorOne(Interface): pass
        >>> class IBehaviorTwo(Interface): pass
    
        >>> from zope.component import provideUtility
        >>> from plone.behavior.registration import BehaviorRegistration

        >>> b1 = BehaviorRegistration("Behavior 1", "", IBehaviorOne, None)
        >>> b2 = BehaviorRegistration("Behavior 2", "", IBehaviorTwo, None)

        >>> provideUtility(b1, name="b1")
        >>> provideUtility(b2, name="b2")
    
    Now let's test the registry. To begin with, we have nothing registered:
    
        >>> from plone.behavior.registry import PersistentBehaviorRegistry
        >>> registry = PersistentBehaviorRegistry()
        
        >>> list(registry.enumerate(IOne))
        []

        >>> registry.is_registered(IOne, IBehaviorOne)
        False
        
        >>> registry.unregister(IOne, IBehaviorOne) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: <InterfaceClass plone.behavior.registry.IOne>
        
        
    When we register one behavior, we will be able to enumerate it, assert the
    registration, and eventually unregister it.
    
        >>> registry.register(IOne, IBehaviorOne)
        >>> registry.register(ITwo, IBehaviorOne)
        >>> registry.register(ITwo, IBehaviorTwo)

        >>> list(registry.enumerate(IOne))
        [<InterfaceClass plone.behavior.registry.IBehaviorOne>]
        
        >>> list(registry.enumerate(ITwo))
        [<InterfaceClass plone.behavior.registry.IBehaviorOne>, <InterfaceClass plone.behavior.registry.IBehaviorTwo>]
        
        >>> registry.is_registered(IOne, IBehaviorOne)
        True
        
        >>> registry.unregister(IOne, IBehaviorOne)
        
        >>> registry.is_registered(IOne, IBehaviorOne)
        False
        
    Unregistering twice is not supported.
    
        >>> registry.unregister(IOne, IBehaviorOne) # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        KeyError: <InterfaceClass plone.behavior.registry.IBehaviorOne>
    """
    implements(IBehaviorRegistry)

    _behaviors = OOBTree() # interface -> set(names)
    
    def register(self, interface, behavior_name):
        self._behaviors.setdefault(interface, OOSet()).insert(behavior_name)
        
    def unregister(self, interface, behavior_name):
        behaviors = self._behaviors[interface]
        behaviors.remove(behavior_name)
    
    def is_registered(self, interface, behavior_name):
        return behavior_name in self._behaviors.get(interface, set())
    
    def enumerate(self, interface):
        return self._behaviors.get(interface, set())