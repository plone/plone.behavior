from zope.interface import Interface
from zope import schema
from zope.configuration.fields import GlobalObject, GlobalInterface

class IBehaviorAssignable(Interface):
    """An object will be adapted to this interface to determine if it supports
    one or more behaviors.
    
    There is no default implementation of this adapter. The mechanism for 
    assigning behaiors to an object or type of object is application specific.
    """
    
    def supports(behavior_interface):
        """Determine if the context supports the given behavior, returning
        True or False.
        """
        
    def enumerate_behaviors():
        """Return an iterable of all the interfaces of the behaviors supported by 
        the context.
        """

class IBehavior(Interface):
    """A description of a behavior. These should be registered as named 
    utilities. There should also be an adapter factory registered, probably
    using IBehaviorAdapterFactory.
    """

    title = schema.TextLine(title=u"Short title of the behavior",
                            required=True)
    
    description = schema.Text(title=u"Longer description of the behavior",
                              required=False)

    interface = GlobalInterface(title=u"Interface describing this behavior")

    factory = GlobalObject(title=u"An adapter factory for the behavior",
                           required=True)

class IBehaviorAdapterFactory(Interface):
    """An adapter factory that wraps a given behavior's own factory. By
    registering an adapter from Interface (or some other general source) to
    the behavior's interface that uses this factory, we can easily support
    the following semantics:
    
        context = SomeObject()
        behavior_adapter = ISomeBehavior(context, None)
     
     The ISomeBehavior adapter factory (i.e. the object providing 
     IBehaviorAdapterFactory) will return None if
     IBehaviorAssignable(context).supports(ISomeBehavior) is False, or if
     the context cannot be adapted to IBehaviorAssignable at all.
    """
    
    behavior = GlobalObject(title=u"The behavior this is a factory for")
    
    def __call__(context):
        """Invoke the behavior-specific factory if the context can be adapted
        to IBehaviorAssignable and 
        IBehaviorAssignable(context).supports(self.behavior.interface) returns
        True.
        """
        
class IBehaviorRegistry(Interface):
    """A registry of behaviors that looks up behaviors by interface
    """
    
    def register(interface, behavior_interface):
        """Register a new behavior for the given interface.
        """
        
    def unregister(interface, behavior_interface):
        """Unregister a behavior for the given interface.
        """
    
    def is_registered(interface, behavior_interface):
        """Return True or False to indicate whether the given behavior is
        registerd for the given interface.
        """
    
    def enumerate(interface):
        """Yield behavior interfaces for a given interface.
        """
