==================================
plone.behavior: Annotation storage
==================================

``plone.behavior`` comes with a standard behavior factory that can be used to
store the data of a schema interface in annotations. This means that it is
possible to create a simple "data only" behavior with just an interface.

We have created such an interface in ``plone.behavior.tests``, called
``IAnnotationStored``. It has a single field, 'some_field'.

Let's show how this may be registered in ZCML::

    >>> configuration = u"""\
    ... <configure
    ...      xmlns="http://namespaces.zope.org/zope"
    ...      xmlns:plone="http://namespaces.plone.org/plone"
    ...      i18n_domain="plone.behavior.tests">
    ...
    ...     <include package="zope.component" file="meta.zcml" />
    ...     <include package="plone.behavior" file="meta.zcml" />
    ...     <include package="zope.annotation" />
    ...
    ...     <plone:behavior
    ...         title="Annotation behavior"
    ...         provides="plone.behavior.tests.IAnnotationStored"
    ...         factory="plone.behavior.AnnotationStorage"
    ...         />
    ...
    ... </configure>
    ... """

    >>> try:
    ...     from io import StringIO
    ... except ImportError:
    ...     from StringIO import StringIO
    >>> from zope.configuration import xmlconfig
    >>> xmlconfig.xmlconfig(StringIO(configuration))

Let us now test this. First, we'll need an annotatable context and an
``IBehaviorAssignable`` adapter. See ``behaviors.rst`` for more details::

    >>> from plone.behavior.interfaces import  IBehaviorAssignable
    >>> from plone.behavior.interfaces import IBehavior
    >>> from plone.behavior.tests import IAnnotationStored
    >>> from zope.annotation.interfaces import IAnnotations
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> from zope.component import adapter
    >>> from zope.component import getUtility
    >>> from zope.component import provideAdapter
    >>> from zope.interface import Interface
    >>> from zope.interface import alsoProvides
    >>> from zope.interface import implementer
    >>> BEHAVIORS = {}

    >>> @implementer(IBehaviorAssignable)
    ... @adapter(Interface)
    ... class TestingBehaviorAssignable(object):
    ...
    ...     def __init__(self, context):
    ...         self.context = context
    ...
    ...     def supports(self, behavior_interface):
    ...         global BEHAVIORS
    ...         return behavior_interface in BEHAVIORS.get(self.context.__class__, [])
    ...
    ...     def enumerateBehaviors(self):
    ...         global BEHAVIORS
    ...         for iface in BEHAVIORS.get(self.context.__class__, []):
    ...             yield getUtility(IBehavior, iface.__identifier__)

    >>> provideAdapter(TestingBehaviorAssignable)

    >>> @implementer(IAttributeAnnotatable)
    ... class Context(object):
    ...     pass
    >>> BEHAVIORS[Context] = [IAnnotationStored]

    >>> context = Context()

We can now adapt the context to our new interface::

    >>> adapted = IAnnotationStored(context)

Before we've set anything, we get the field's missing_value::

    >>> adapted.some_field is IAnnotationStored['some_field'].missing_value
    True

Let's look at the annotations also::

    >>> sorted(IAnnotations(context).items())
    []

If we now set the value, it will be stored in annotations::

    >>> adapted.some_field = u'New value'
    >>> sorted(IAnnotations(context).items())
    [('plone.behavior.tests.IAnnotationStored.some_field', u'New value')]

And of course we can get it back again::

    >>> adapted.some_field
    u'New value'

If we try to get some other field, we get an AttributeError::

    >>> adapted.bogus_field #doctest: +ELLIPSIS
    Traceback (most recent call last):
    ...
    AttributeError: bogus_field

Of course, we can still set and then get some value on the adapter factory
itself, but it won't be persisted::

    >>> adapted.bogus_field = 123
    >>> adapted.bogus_field
    123
