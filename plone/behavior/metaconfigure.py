# -*- coding: utf-8 -*-
from plone.behavior import logger
from plone.behavior.factory import BehaviorAdapterFactory
from plone.behavior.interfaces import IBehavior
from plone.behavior.interfaces import ISchemaAwareFactory
from plone.behavior.registration import BehaviorRegistration
from zope.component.zcml import adapter
from zope.component.zcml import utility
from zope.configuration import fields as configuration_fields
from zope.configuration.exceptions import ConfigurationError
from zope.interface import Interface
from zope.schema import TextLine


class IBehaviorDirective(Interface):
    """Directive which registers a new behavior type.

    The registration consists of:

        * a global named utility registered by interface identifier
        * a global named utility registered by lookup name
        * an associated global and unnamed behavior adapter
    """

    name = TextLine(
        title=u"Name",
        description=u"Convenience lookup name for this behavior",
        required=False)

    title = configuration_fields.MessageID(
        title=u"Title",
        description=u"A user friendly title for this behavior",
        required=True)

    description = configuration_fields.MessageID(
        title=u"Description",
        description=u"A longer description for this behavior",
        required=False)

    provides = configuration_fields.GlobalInterface(
        title=u"An interface to which the behavior can be adapted",
        description=u"This is what the conditional adapter factory will "
                    u"be registered as providing",
        required=True)

    marker = configuration_fields.GlobalInterface(
        title=u"A marker interface to be applied by the behavior",
        description=u"If factory is not given, then this is optional",
        required=False)

    factory = configuration_fields.GlobalObject(
        title=u"The factory for this behavior",
        description=u"If this is not given, the behavior is assumed to "
                    u"provide a marker interface",
        required=False)

    for_ = configuration_fields.GlobalObject(
        title=u"The type of object to register the conditional adapter "
              u"factory for",
        description=u"This is optional - the default is to register the "
                    u"factory for zope.interface.Interface",
        required=False)


def behaviorDirective(_context, title, provides, name=None, description=None,
                      marker=None, factory=None, for_=None):
    if marker is None and factory is None:
        marker = provides

    if marker is not None and factory is None and marker is not provides:
        raise ConfigurationError(
            u"You cannot specify a different 'marker' and 'provides' if "
            u"there is no adapter factory for the provided interface."
        )

    # Instantiate the real factory if it's the schema-aware type. We do
    # this here so that the for_ interface may take this into account.
    if factory is not None and ISchemaAwareFactory.providedBy(factory):
        factory = factory(provides)

    registration = BehaviorRegistration(
        title=title,
        description=description,
        interface=provides,
        marker=marker,
        factory=factory,
        name=name,
    )

    # behavior registration by provides interface identifier
    utility(
        _context,
        provides=IBehavior,
        name=provides.__identifier__,
        component=registration
    )

    if name is not None:
        # for convinience we register with a given name
        utility(
            _context,
            provides=IBehavior,
            name=name,
            component=registration
        )

    if factory is None:
        if for_ is not None:
            logger.warn(
                u"Specifying 'for' in behavior '{0}' if no 'factory' is given "
                u"has no effect and is superfluous.".format(title)
            )
        # w/o factory we're done here
        return

    if for_ is None:
        # Attempt to guess the factory's adapted interface and use it as
        # the 'for_'.
        # Fallback to '*' (=Interface).
        adapts = getattr(factory, '__component_adapts__', None) or [Interface]
        if len(adapts) != 1:
            raise ConfigurationError(
                u"The factory can not be declared as multi-adapter."
            )
        for_ = adapts[0]

    adapter_factory = BehaviorAdapterFactory(registration)

    adapter(
        _context,
        factory=(adapter_factory,),
        provides=provides,
        for_=(for_,)
    )
