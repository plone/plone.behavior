===============================
plone.behavior: ZCML directives
===============================

plone.behavior defines a ZCML directive, in meta.zcml as usual.

For the purpose of this test, we have defined a few dummy behaviors in
plone.behavior.tests:

  * A standard behavior with an interface and a factory. It will be registered
    for any context.

  * An adapter behavior with a factory and an explicit context restriction.

  * An adapter behavior where a context restriction is implied by the
    adapts() declaration on the factory.

  * A behavior with a marker marker interface.

  * A behavior using the standard annotation factory

  * A behavior providing a marker interface and using an adapter factory.

  * A behavior registered by name only

::

    >>> configuration = u"""\
    ... <configure
    ...      package="plone.behavior"
    ...      xmlns="http://namespaces.zope.org/zope"
    ...      xmlns:plone="http://namespaces.plone.org/plone"
    ...      i18n_domain="plone.behavior.tests">
    ...
    ...     <include package="plone.behavior" file="meta.zcml" />
    ...
    ...     <plone:behavior
    ...         name="adapter_behavior"
    ...         title="Adapter behavior"
    ...         description="A basic adapter behavior"
    ...         provides=".tests.IAdapterBehavior"
    ...         factory=".tests.AdapterBehavior"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="context_restricted_behavior"
    ...         title="Context restricted behavior"
    ...         provides=".tests.IRestrictedAdapterBehavior"
    ...         factory=".tests.RestrictedAdapterBehavior"
    ...         for=".tests.IMinimalContextRequirements"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="factory_implied_context_restricted_behavior"
    ...         title="Factory-implied context restricted behavior"
    ...         provides=".tests.IImpliedRestrictionAdapterBehavior"
    ...         factory=".tests.ImpliedRestrictionAdapterBehavior"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="marker_interface_behavior"
    ...         title="Marker interface behavior"
    ...         provides=".tests.IMarkerBehavior"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="annotation_storage_behavior"
    ...         title="Annotation storage behavior"
    ...         provides=".tests.IAnnotationStored"
    ...         factory="plone.behavior.AnnotationStorage"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="marker_and_adapter"
    ...         title="Marker and adapter"
    ...         provides=".tests.IMarkerAndAdapterBehavior"
    ...         factory="plone.behavior.AnnotationStorage"
    ...         marker=".tests.IMarkerAndAdapterMarker"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="marker_and_adapter_no_atadapter"
    ...         title="Marker and adapter no @adapter"
    ...         provides=".tests.IMarkerAndAdapterBehavior2"
    ...         factory=".tests.DummyBehaviorImpl"
    ...         marker=".tests.IMarkerAndAdapterMarker2"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="name_only"
    ...         name_only="yes"
    ...         title="Marker interface behavior"
    ...         provides=".tests.INameOnlyBehavior"
    ...         />
    ...
    ...     <plone:behavior
    ...         name="renamed_adapter_behavior"
    ...         title="Renamed Adapter behavior"
    ...         description="A basic adapter behavior that used to have a different name"
    ...         provides=".tests.IRenamedAdapterBehavior"
    ...         factory=".tests.RenamedAdapterBehavior"
    ...         former_dotted_names="plone.behavior.tests.IOriginalAdapterBehavior"
    ...         />
    ...
    ... </configure>
    ... """

Let's first verify that we don't have the dummy data registered already:

    >>> from zope.component import getGlobalSiteManager
    >>> sm = getGlobalSiteManager()

    >>> from plone.behavior.interfaces import IBehavior
    >>> [u for u in sm.registeredUtilities() if u.name == u"plone.behavior.tests.IAdapterBehavior"]
    []

    >>> from plone.behavior.tests import IAdapterBehavior
    >>> [a for a in sm.registeredAdapters() if a.provided == IAdapterBehavior]
    []

We should now be able to load the sample configuration, which also includes the
meta.zcml file from plone.behavior:

    >>> try:
    ...     from io import StringIO
    ... except ImportError:
    ...     from StringIO import StringIO
    >>> from zope.configuration import xmlconfig
    >>> xmlconfig.xmlconfig(StringIO(configuration))

With this in place, the behaviors should be registered, e.g:

    >>> from plone.behavior.interfaces import IBehavior
    >>> sorted([u for u in sm.registeredUtilities() if u.name == u"plone.behavior.tests.IAdapterBehavior"]) # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    [UtilityRegistration(<BaseGlobalComponents base>, IBehavior, 'plone.behavior.tests.IAdapterBehavior', <BehaviorRegistration adapter_behavior at ...
      schema: plone.behavior.tests.IAdapterBehavior
      marker: (no marker is set)
      factory: <class 'plone.behavior.tests.AdapterBehavior'>
      title: Adapter behavior
      A basic adapter behavior
    ...UtilityRegistration(<BaseGlobalComponents base>, IInterface, 'plone.behavior.tests.IAdapterBehavior', IAdapterBehavior, None, '')]

    >>> from plone.behavior.tests import IAdapterBehavior
    >>> [a for a in sm.registeredAdapters() if a.provided == IAdapterBehavior]  # doctest: +ELLIPSIS
    [AdapterRegistration(..., [Interface], IAdapterBehavior,..., <plone.behavior.factory.BehaviorAdapterFactory object at ...>, ...)]

Let us test the various utilities and the underlying adapters more carefully.

    >>> from zope.component import getUtility
    >>> from plone.behavior.interfaces import IBehavior

1) A standard behavior with an interface and a factory. It will be registered
for any context.

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IAdapterBehavior")
    >>> dummy.name
    u'adapter_behavior'

    >>> dummy.title
    u'Adapter behavior'

    >>> dummy.description
    u'A basic adapter behavior'

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IAdapterBehavior>

    >>> dummy.marker is None
    True

    >>> dummy.factory
    <class 'plone.behavior.tests.AdapterBehavior'>

    >>> from plone.behavior.tests import IAdapterBehavior
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IAdapterBehavior][0]
    (<InterfaceClass zope.interface.Interface>,)

2) An adapter behavior with a factory and an explicit context restriction.

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IRestrictedAdapterBehavior")
    >>> dummy.name
    u'context_restricted_behavior'

    >>> dummy.title
    u'Context restricted behavior'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IRestrictedAdapterBehavior>

    >>> dummy.marker is None
    True

    >>> dummy.factory
    <class 'plone.behavior.tests.RestrictedAdapterBehavior'>

    >>> from plone.behavior.tests import IRestrictedAdapterBehavior
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IRestrictedAdapterBehavior][0]
    (<InterfaceClass plone.behavior.tests.IMinimalContextRequirements>,)

3) An adapter behavior where a context restriction is implied by the adapts()
declaration on the factory.

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IImpliedRestrictionAdapterBehavior")
    >>> dummy.name
    u'factory_implied_context_restricted_behavior'

    >>> dummy.title
    u'Factory-implied context restricted behavior'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IImpliedRestrictionAdapterBehavior>

    >>> dummy.marker is None
    True

    >>> dummy.factory
    <class 'plone.behavior.tests.ImpliedRestrictionAdapterBehavior'>

    >>> from plone.behavior.tests import IImpliedRestrictionAdapterBehavior
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IImpliedRestrictionAdapterBehavior][0]
    (<InterfaceClass plone.behavior.tests.ISomeContext>,)

4) A behavior with a marker marker interface.

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IMarkerBehavior")
    >>> dummy.name
    u'marker_interface_behavior'

    >>> dummy.title
    u'Marker interface behavior'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IMarkerBehavior>

    >>> dummy.marker
    <InterfaceClass plone.behavior.tests.IMarkerBehavior>

    >>> dummy.factory is None
    True

    >>> from plone.behavior.tests import IMarkerBehavior
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IMarkerBehavior]
    []

5) A behavior using the standard annotation factory

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IAnnotationStored")
    >>> dummy.name
    u'annotation_storage_behavior'

    >>> dummy.title
    u'Annotation storage behavior'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IAnnotationStored>

    >>> dummy.marker is None
    True

    >>> dummy.factory # doctest: +ELLIPSIS
    <plone.behavior.annotation.AnnotationStorage object at ...>

    >>> from plone.behavior.tests import IAnnotationStored
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IAnnotationStored][0]
    (<InterfaceClass zope.annotation.interfaces.IAnnotatable>,)

6) A behavior providing a marker interface and using an adapter factory.

6.1) ``@adapter`` decorated Behavior implementation.

    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IMarkerAndAdapterBehavior")
    >>> dummy.name
    u'marker_and_adapter'

    >>> dummy.title
    u'Marker and adapter'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IMarkerAndAdapterBehavior>

    >>> dummy.marker
    <InterfaceClass plone.behavior.tests.IMarkerAndAdapterMarker>

    >>> dummy.factory # doctest: +ELLIPSIS
    <plone.behavior.annotation.AnnotationStorage object at ...>

    The factory has ist ``__component_adapts__`` (``@adapter``) in place, so the adapted Interface must be returned.

    >>> from plone.behavior.tests import IMarkerAndAdapterBehavior
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IMarkerAndAdapterBehavior][0]
    (<InterfaceClass zope.annotation.interfaces.IAnnotatable>,)


6.2) non ``@adapter`` decorated Behavior implementation.

    >>> dummy = getUtility(IBehavior, name=u"marker_and_adapter_no_atadapter")
    >>> dummy.name
    u'marker_and_adapter_no_atadapter'

    >>> dummy.title
    u'Marker and adapter no @adapter'

    >>> dummy.description is None
    True

    >>> dummy.interface
    <InterfaceClass plone.behavior.tests.IMarkerAndAdapterBehavior2>

    >>> dummy.marker
    <InterfaceClass plone.behavior.tests.IMarkerAndAdapterMarker2>

    >>> dummy.factory # doctest: +ELLIPSIS
    <class 'plone.behavior.tests.DummyBehaviorImpl'>

    The factory has ist ``__component_adapts__`` (``@adapter``) in place, so the adapted Interface must be returned.

    >>> from plone.behavior.tests import IMarkerAndAdapterBehavior2
    >>> [a.required for a in sm.registeredAdapters() if a.provided == IMarkerAndAdapterBehavior2][0]
    (<InterfaceClass plone.behavior.tests.IMarkerAndAdapterMarker2>,)


7) A name only registered behavior

    >>> from zope.interface.interfaces import ComponentLookupError
    >>> failed = False
    >>> try:
    ...     dummy = getUtility(IBehavior, name=u"plone.behavior.tests.INameOnlyBehavior")
    ... except ComponentLookupError as e:
    ...     failed = True
    >>> failed
    True

    >>> dummy = getUtility(IBehavior, name=u"name_only")
    >>> dummy.name
    u'name_only'

8) A behavior that used to be known under a different dotted name

    A behavior that has been renamed, can of course be found under the new name.
    The representation tells us the former dotted name.
    
    >>> dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IRenamedAdapterBehavior")
    >>> dummy  # doctest: +ELLIPSIS
    <BehaviorRegistration renamed_adapter_behavior at ...
      schema: plone.behavior.tests.IRenamedAdapterBehavior
      marker: (no marker is set)
      factory: <class 'plone.behavior.tests.RenamedAdapterBehavior'>
      title: Renamed Adapter behavior
      A basic adapter behavior that used to have a different name
      former dotted names: plone.behavior.tests.IOriginalAdapterBehavior
    >

Test registration lookup helper utility.

    >>> from plone.behavior.registration import lookup_behavior_registration
    >>> lookup_behavior_registration()
    Traceback (most recent call last):
      ...
    ValueError: Either ``name`` or ``identifier`` must be given

    >>> lookup_behavior_registration('inexistent')
    Traceback (most recent call last):
      ...
    BehaviorRegistrationNotFound: inexistent

    >>> lookup_behavior_registration('adapter_behavior')  # doctest: +ELLIPSIS
    <BehaviorRegistration adapter_behavior at ...
      schema: plone.behavior.tests.IAdapterBehavior
      marker: (no marker is set)
      factory: <class 'plone.behavior.tests.AdapterBehavior'>
      title: Adapter behavior
      A basic adapter behavior
    >

    >>> lookup_behavior_registration(
    ...     identifier='plone.behavior.tests.IAdapterBehavior'
    ... )  # doctest: +ELLIPSIS
    <BehaviorRegistration adapter_behavior at ...
      schema: plone.behavior.tests.IAdapterBehavior
      marker: (no marker is set)
      factory: <class 'plone.behavior.tests.AdapterBehavior'>
      title: Adapter behavior
      A basic adapter behavior
    >

    A lookup via getUtility for a former behavior name fails.
    
    >>> failed = False
    >>> try:
    ...     dummy = getUtility(IBehavior, name=u"plone.behavior.tests.IOriginalAdapterBehavior")
    ... except ComponentLookupError:
    ...     failed = True
    >>> failed
    True

    But the lookup helper still finds it under the former name.
    
    >>> dummy = lookup_behavior_registration("plone.behavior.tests.IOriginalAdapterBehavior")
    >>> dummy.name
    u'renamed_adapter_behavior'
