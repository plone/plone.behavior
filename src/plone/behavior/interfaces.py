from zope import schema
from zope.interface import Interface
from zope.interface.interfaces import IInterface


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

    def enumerateBehaviors():
        """Return an iterable of all the IBehaviors supported by the context."""


class IBehavior(Interface):
    """A description of a behavior. These should be registered as named
    utilities. There should also be an adapter factory registered, probably
    using IBehaviorAdapterFactory.
    """

    title = schema.TextLine(
        title="Short title of the behavior",
        required=True,
    )

    description = schema.Text(
        title="Longer description of the behavior",
        required=False,
    )

    name = schema.TextLine(
        title="Readable short name to be used for behavior lookup",
        description="E.g. plone.somebehavior. If not given the full dotted "
        "name of the interfaces is used for lookup instead."
        "Recommended, but due to BBB not required.",
        required=False,
    )

    interface = schema.Object(
        title="Interface describing this behavior",
        required=True,
        schema=IInterface,
    )

    marker = schema.Object(
        title="Marker interface for objects sporting this behavior",
        description="Markers are persisted in the ZODB. "
        "Required when a factory is given, because the factory "
        "is an adapter adapting the the marker and providing the "
        '"interface" of this behavior.',
        required=False,
        schema=IInterface,
    )

    factory = schema.Object(
        title="An adapter factory for the behavior",
        required=True,
        schema=Interface,
    )


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

    behavior = schema.Object(
        title="The behavior this is a factory for",
        schema=IBehavior,
    )

    def __call__(context):
        """Invoke the behavior-specific factory if the context can be adapted
        to IBehaviorAssignable and
        IBehaviorAssignable(context).supports(self.behavior.interface) returns
        True.
        """


class ISchemaAwareFactory(Interface):
    """Marker interface for factories that should be initialised with a
    schema. The factory must be a callable that takes the schema as an
    argument and returns another callable that can create appropriate behavior
    factories on demand.

    See annotation.py for an example.
    """
