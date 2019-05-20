==============
plone.behavior
==============

.. contents:: Table of Contents
   :depth: 2


Overview
========

This package provides support for **behaviors**.

    A behavior is a re-usable aspect of an object that can be enabled or disabled without changing the component registry.

A behavior is described by an interface, and has metadata such as a title and a description.
The behavior can be looked up by a given short name or by the dotted name of the interface.
With this unique name behaviors metadata can be looked up.
When the behavior is enabled for an object, you will be able to adapt the object to the interface.
In some cases, the interface can be used as a marker interface as well.

As an example, let's say that your application needs to support object-level locking.
This can be modeled via an adapter, but you want to leave it until runtime to determine whether locking is enabled for a particular object.
You could then register locking as a behavior.

**Requirements and Limitations:**

* This package comes with support for registering behaviors and factories.

* It does not implement the policy for determining what behaviors are enabled on a particular object at a particular time.
  That decision is deferred to an ``IBehaviorAssignable`` adapter, which must be implemented (``plone.dexterity`` implements this).

* Like the ``IBehaviorAssignable`` plumbing, marker interface support needs to be enabled on a per-application basis.
  This package also does not directly support the adding of marker interfaces to instances.
  To do that, you can either use an event handler to mark an object when it is created, or a dynamic __providedBy__ descriptor that does the lookup on the fly (but you probably want some caching).
  A sample event handler is provided with this package, but is not registered by default

* The intention is that behavior assignment is generic across an application, used for multiple, optional behaviors.
  It probably doesn't make much sense to use ``plone.behavior`` for a single type of object.
  The means to keep track of which behaviors are enabled for what types of objects will be application specific.

Usage
=====

Explained
---------

A behavior is written much like an adapter, except that you don't specify the type of context being adapted directly.
For example::

    from zope.interface import Interface
    from zope.interface import implementer

    class ILockingSupport(Interface):
       """Support locking
       """

       def lock():
           """Lock an object
           """

       def unlock():
           """Unlock an object
           """

    @implementer(ILockingSupport)
    class LockingSupport(object):

        def __init__(self, context):
            self.context = context

        def lock(self):
            # do something

        def unlock(self):
            # do something

This interface (which describes the type of behavior) and class (which describes the implementation of the behavior) then needs to be registered.

The simplest way to do that is to load the ``meta.zcml`` file from this package and use ZCML::

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:plone="http://namespaces.plone.org/plone"
      i18n_domain="my.package">

      <include package="plone.behavior" file="meta.zcml" />

      <plone:behavior
          name="locking_support"
          title="Locking support"
          description="Optional object-level locking"
          provides=".interfaces.ILockingSupport"
          factory=".locking.LockingSupport"
      />

    </configure>

After this is done you can adapt a context to ``ILockingSupport`` as normal::

    locking = ILockingSupport(context, None)

    if locking is not None:
        locking.lock()

The ``name`` can be used for lookup instead of the full dotted name of the interface::

    from plone.behavior.interfaces import IBehavior
    from zope.component import getUtility

    registration = getUtility(IBehavior, name='locking_support')

We also have a helper function to achieve this::

    from plone.behavior.registration import lookup_behavior_registration

    registration = lookup_behavior_registration(name='locking_support')


You'll get an instance of ``LockingSupport`` if context can be adapted to ``IBehaviorAssignable`` (which, recall, is application specific),
and if the implementation of ``IBehaviorAssignable`` says that this context supports this particular behavior.

It is also possible to let the provided interface act as a marker interface that is to be provided directly by the instance.
To achieve this, omit the ``factory`` argument.
This is useful if you need to register other adapters for instances providing a particular behavior.

ZCML Reference
--------------

The ``plone:behavior`` directive uses the namespace ``xmlns:plone="http://namespaces.plone.org/plone"``.
In order to enable it loading of its ``meta.zcml`` is needed, use::

    <include package="plone.behavior" file="meta.zcml" />

The directive supports the attributes:

``title``
    A user friendly title for this behavior (required).

``description``
    A longer description for this behavior (optional).

``provides``
    An interface to which the behavior can be adapted.
    This is what the conditional adapter factory will be registered as providing (required).

``name``
    Convenience lookup name for this behavior (optional).
    The behavior will be always registered under the dotted name of ``provides`` attribute.
    This are usally long names. ``name`` is a short name for this.
    If ``name`` is given the behavior is registered additional under it.
    Anyway using short namespaces in ``name`` is recommended.

``name_only``
    If set to ``yes`` or ``true`` the behavior is registered only under the given name,
    but not under the dotted path of the ``provides`` interface.
    This makes ``name`` mandatory.

``marker``
    A marker interface to be applied by the behavior.
    If ``factory`` is not given, then this is optional and defaults to the value of ``provides``.
    If factory is given ``marker`` is required and should be different from ``provides`` - even if its not enforced.

``factory``
    The factory for this behavior (optional).
    If no factory is given, the behavior context is assumed to provide the interface given by ``provides`` itself.

    If factory provides ``plone.behavior.interfaces.ISchemaAwareFactory`` the factory is assumed to be a callable.
    ``ISchemaAwareFactory`` is an interface for factories that should be initialised with a schema.
    It is called with the value given in ``provides`` as the only argument.
    The value returned is then used as the factory, another callable that can create appropriate behavior factories on demand.

``for``
    The type of object to register the conditional adapter factory for (optional).
    Must be omitted is no ``factory`` is given.

    The default is either to auto-detect what the factory adapts (i.e. using the ``@adapter`` decorator) or to fall back to ``zope.interface.Interface`` (also written as ``*`` in ZCML).

    Must be one element (no multiadapters, applies also for auto-detection).

``former_dotted_names``
    In case a behavior is modified so that its dotted name changes, this field can be used to register the old name(s). Therefore, it is possible to retrieve the name(s) under which a behavior was formerly registered under.

    If a call to ``lookup_behavior_registration`` does not find a behavior under the given name, it will look at the former dotted names to try and find the behavior.


ZCML Examples
-------------

Example usage, given

- some ``context`` (some arbitary object) which is ``IBehaviorAssignable``,
- an ``IMyBehavior`` interface intented to be used as ``provides``,
- an ``IMyMarker`` interface intented to be used as ``marker``,
- a ``MyFactory`` class implementing ``IMyBehavior`` ,
- a ``MySchemaAwareFactory`` class implementing ``IMyBehavior`` and ``plone.behavior.interfaces.ISchemaAwareFactory``,
- an ``IMyType`` intented to be used as ``for``.
- some ``typed_context`` (some arbitary object) which is ``IBehaviorAssignable`` and provides ``IMyType``,
- an ``MyTypedFactory`` class implementing ``IMyBehavior`` and adapting ``IMyType``,

``title`` and ``description`` is trivial, so we dont cover it here in the explanantion.
We dont cover ``name`` too, because it's not having any effect in this usage.
To simplify it, we assume ``context`` ``IBehaviorAssignable`` always supports the behavior.
Also for simplifications sake we assume some magic applies the marker interface to ``context``
I.e. both is done by ``plone.dexterity``.

**Example 1** - only ``provides`` given::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
    />

- ``marker`` defaults to ``provides``,
- with ``behavior = IMyBehavior(context)`` the ``context`` itself is returned,
- ``context`` provides ``IBehavior``,

**Example 2** - also ``factory`` is given, so ``marker`` is required:

.. warning::
   Using the same Interface as marker and behavior works, but is not recommended and will be deprecated in future.
   It is semantically wrong!
   
   Go for Example 3 instead!

::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
        marker="IMyBehavior"
        factory="MyFactory"
    />

- ``marker`` is the same as ``provides``,
- with ``behavior = IMyBehavior(context)`` a ``MyFactory`` instance is returned,
- ``context`` provides ``IMyBehavior``,
- ``MyFactory`` instance provides ``IMyBehavior``,
- having ``context`` and ``MyFactory`` providing both the same interface is ugly and not recommended!

**Example 3** - in example 2 both, factory and context are providing the ``IMyBehavior``.
This may lead to confusion, so now better with a ``marker``::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
        marker="IMyMarker"
        factory="MyFactory"
    />

- with ``behavior = IMyBehavior(context)`` a ``MyFactory`` instance is returned,
- ``context`` provides ``IMyMarker``,
- ``MyFactory`` instance provides ``IMyBehavior``,

**Example 4** - like example 3 but with an ``MySchemaAwareFactory``::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
        marker="IMyMarker"
        factory="MySchemaAwareFactory"
    />

- with ``behavior = IMyBehavior(context)`` some factory instance is returned as a result from calling a ``MySchemaAwareFactory`` instance with ``IMyBehavior`` as argument,
- ``context`` provides ``IMyMarker``,
- ``MyFactory`` instance provides ``IMyBehavior``,

**Example 5** - the behavior should be restricted to the ``typed_context``::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
        marker="IMyMarker"
        factory="MyFactory"
        for="IMyType"
    />

- with ``behavior = IMyBehavior(context, None)`` it could not adapt and ``behavior`` is ``None``,
- with ``behavior = IMyBehavior(typed_context)`` a ``MyFactory`` instance is returned,
- ``context`` provides ``IMyMarker``,
- ``MyFactory`` provides ``IMyBehavior``,

**Example 6** - the behavior should be restricted to the ``typed_context`` by auto-detection.
The ``MyTypedFactory`` class adapts ``IMyType`` using a class decorator ``@adapter(IMyType)``::

    <plone:behavior
        title="Example 1"
        provides="IMyBehavior"
        marker="IMyMarker"
        factory="MyTypedFactory"
    />

- with ``behavior = IMyBehavior(context, None)`` it could not adapt and ``behavior`` is ``None``,
- with ``behavior = IMyBehavior(typed_context)`` a ``MyFactory`` instance is returned,
- ``context`` provides ``IMyMarker``,
- ``MyFactory`` instance provides ``IMyBehavior``,


Further Reading
---------------

For more details please read the doctests in the source code: ``behavior.rst``, ``directives.rst`` and ``annotation.rst``.


Source Code
===========

Contributors please read the document `Process for Plone core's development <https://docs.plone.org/develop/coredev/docs/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.behavior>`_.
