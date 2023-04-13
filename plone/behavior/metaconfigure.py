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
        title="Name",
        description="Convenience lookup name for this behavior",
        required=False,
    )

    title = configuration_fields.MessageID(
        title="Title",
        description="A user friendly title for this behavior",
        required=True,
    )

    description = configuration_fields.MessageID(
        title="Description",
        description="A longer description for this behavior",
        required=False,
    )

    provides = configuration_fields.GlobalInterface(
        title="An interface to which the behavior can be adapted",
        description="This is what the conditional adapter factory will "
        "be registered as providing",
        required=True,
    )

    marker = configuration_fields.GlobalInterface(
        title="A marker interface to be applied by the behavior",
        description="If factory is not given, then this is optional",
        required=False,
    )

    factory = configuration_fields.GlobalObject(
        title="The factory for this behavior",
        description="If this is not given, the behavior is assumed to "
        "provide a marker interface",
        required=False,
    )

    for_ = configuration_fields.GlobalObject(
        title="The type of object to register the conditional adapter " "factory for",
        description="This is optional - the default is to register the "
        "factory for zope.interface.Interface",
        required=False,
    )

    name_only = configuration_fields.Bool(
        title="Do not register the behavior under the dotted path, but "
        "only under the given name",
        description="Use this option to register a behavior for the same "
        "provides under a different name.",
        required=False,
    )

    former_dotted_names = TextLine(
        title="Space-separated list of dotted names that this behavior was "
        "formerly registered under",
        description="Use this field in case you change the dotted name, "
        "so that the current behavior can be looked up under "
        "its former name.",
        required=False,
    )


def _detect_for(factory, marker):
    """if no explicit for is given we need to figure it out."""
    # Attempt to guess the factory's adapted interface and use it as
    # the 'for_'.
    # at last bastion fallback to '*' (=Interface).
    adapts = getattr(factory, "__component_adapts__", [])
    if len(adapts) == 1:
        return adapts[0]
    if len(adapts) > 1:
        raise ConfigurationError("The factory can not be declared as multi-adapter.")
    # down here it means len(adapts) < 1
    if marker is not None:
        # given we have a marker it is safe to register for the
        # marker, as the behavior context will always provides it
        return marker
    # fallback: for="*"
    return Interface


def behaviorDirective(
    _context,
    title,
    provides,
    name=None,
    description=None,
    marker=None,
    factory=None,
    for_=None,
    name_only=False,
    former_dotted_names="",
):
    if marker is None and factory is None:
        # a schema only behavior means usually direct attribute settings on the
        # object itself, so the object itself provides the interface.
        # so we mark with the provides.
        marker = provides

    if marker is not None and factory is None and marker is not provides:
        raise ConfigurationError(
            "You cannot specify a different 'marker' and 'provides' if "
            "there is no adapter factory for the provided interface."
        )
    if name_only and name is None:
        raise ConfigurationError(
            "If you decide to only register by 'name', a name must " "be given."
        )

    # Instantiate the real factory if it's the schema-aware type. We do
    # this here so that the for_ interface may take this into account.
    if factory is not None and ISchemaAwareFactory.providedBy(factory):
        factory = factory(provides)

    # the behavior registration hold all information about the behavior.
    registration = BehaviorRegistration(
        title=title,
        description=description,
        interface=provides,
        marker=marker,
        factory=factory,
        name=name,
        former_dotted_names=former_dotted_names,
    )
    # the behavior registration can be looked up as a named utility.
    # the name of the utility is either the full dotted path of the interface
    # it provides...
    if not name_only:
        # behavior registration by provides interface identifier
        utility(
            _context,
            provides=IBehavior,
            name=provides.__identifier__,
            component=registration,
        )

    if name is not None:
        # .. or if given, we register with a given (short) name.
        # Advantage is, we can have more than one implementations of a
        # behavior on one object (if a factory is used).
        # This is handy for certain use cases.
        utility(
            _context,
            provides=IBehavior,
            name=name,
            component=registration,
        )

    if factory is None:
        if for_ is not None:
            logger.warn(
                "Specifying 'for' in behavior '{}' if no 'factory' is "
                "given has no effect and is superfluous.".format(title)
            )
        # w/o factory we're done here: schema only behavior
        return

    if for_ is None:
        for_ = _detect_for(factory, marker)

    adapter_factory = BehaviorAdapterFactory(registration)
    adapter(
        _context,
        factory=(adapter_factory,),
        provides=provides,
        for_=(for_,),
    )
