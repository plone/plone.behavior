from zope.interface import Interface, implementedBy

from zope import schema
from zope.configuration import fields as configuration_fields
from zope.configuration.exceptions import ConfigurationError

from zope.component.zcml import adapter
from zope.component.zcml import utility

from plone.behavior.interfaces import IBehavior
from plone.behavior.interfaces import ISchemaAwareFactory

from plone.behavior.registration import BehaviorRegistration
from plone.behavior.factory import BehaviorAdapterFactory

class IBehaviorDirective(Interface):
    """Directive which registers a new behavior type (a global, named
    utility) and associated behavior adapter factory (a global, unnamed
    adapter)
    """
    
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
        required=False)
        
    subtype = configuration_fields.GlobalInterface(
        title=u"A marker interface to apply to newly created objects supporting this behavior",
        description=u"Only use this if you really need it, e.g. to support view or viewlet registrations.",
        required=False)
    
    factory = configuration_fields.GlobalObject(
        title=u"The factory for this behavior",
        description=u"This is what the conditional adapter factory will return if the behavior is enabled",
        required=False)

    for_ = configuration_fields.GlobalObject(
        title=u"The type of object to register the conditional adapter factory for",
        description=u"This is optional - the default is to register the factory for zope.interface.Interface",
        required=False)
        
def behaviorDirective(_context, title, description=None, interface=None, factory=None,
                      subtype=None, for_=None):
    
    # Attempt to guess the factory's implemented interface and use it as the behavior interface
    
    if interface is None and factory is not None and not ISchemaAwareFactory.providedBy(factory):
        provided = list(implementedBy(factory))
        if len(provided) == 1:
            interface = provided[0]
    elif interface is None and subtype is not None:
        interface = subtype
    
    if interface is None:
        raise ConfigurationError(u"Unable to determine a unique behaviour interface. "
                                  "Use the 'interface' attribute to specify one")

    # Instantiate the real factory if it's the schema-aware type. We do
    # this here so that the for_ interface may take this into account.
    if factory is not None and ISchemaAwareFactory.providedBy(factory):
        factory = factory(interface)
    
    # Attempt to guess the factory's adapted interface and use it as the for_
    if for_ is None and factory is not None:
        adapts = getattr(factory, '__component_adapts__', None)
        if adapts:
            if len(adapts) != 1:
                raise ConfigurationError(u"The factory cannot be declared a multi-adapter.")
            for_ = adapts[0]
        else:
            for_ = Interface
    elif for_ is None:
        for_ = Interface
        

    
    registration = BehaviorRegistration(title=title,
                                        description=description,
                                        interface=interface,
                                        subtype=subtype,
                                        factory=factory)

    adapter_factory = BehaviorAdapterFactory(registration)
    
    utility(_context, 
            provides=IBehavior,
            name=interface.__identifier__,
            component=registration)
            
    adapter(_context, 
            factory=(adapter_factory,),
            provides=interface,
            for_=(for_,))
