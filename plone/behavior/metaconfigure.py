from zope.interface import Interface

from zope import schema
from zope.configuration import fields as configuration_fields

from zope.component.zcml import adapter
from zope.component.zcml import utility

from plone.behavior.interfaces import IBehavior

from plone.behavior.registration import BehaviorRegistration
from plone.behavior.factory import BehaviorAdapterFactory

class IBehaviorDirective(Interface):
    """Directive which registers a new behavior type (a global, named
    utility) and associated behavior adapter factory (a global, unnamed
    adapter)
    """
    
    name = schema.DottedName(
        title=u"Name",
        description=u"A unique name for this behavior",
        required=True)
        
    title = schema.TextLine(
        title=u"Title",
        description=u"A user friendly title for this behavior",
        required=True)
        
    description = schema.Text(
        title=u"Description",
        description=u"A longer description for this behavior",
        required=False)
                           
    interface = configuration_fields.GlobalInterface(
        title=u"The interface describing this behavior",
        description=u"This is what the conditional adapter factory will be registered as providing",
        required=True)
    
    factory = configuration_fields.GlobalObject(
        title=u"The factory for this behavior",
        description=u"This is what the conditional adapter factory will return if the behavior is enabled",
        required=True)

    for_ = configuration_fields.GlobalObject(
        title=u"The type of object to register the conditional adapter factory for",
        description=u"This is optional - the default is to register the factory for zope.interface.Interface",
        required=False)
        
def behaviorDirective(_context, name, title, description, interface, factory, for_=Interface):
    
    registration = BehaviorRegistration(title=title,
                                        description=description,
                                        interface=interface,
                                        factory=factory)

    adapter_factory = BehaviorAdapterFactory(registration)
    
    utility(_context, 
            provides=IBehavior,
            name=name,
            component=registration)
            
    adapter(_context, 
            factory=(adapter_factory,),
            provides=interface,
            for_=(for_,))