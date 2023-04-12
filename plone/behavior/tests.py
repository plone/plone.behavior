from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import doctest
import unittest
import zope.component.testing


# Simple adapter behavior - no context restrictions
class IAdapterBehavior(Interface):
    pass


@implementer(IAdapterBehavior)
class AdapterBehavior:
    def __init__(self, context):
        self.context = context


# Simple adapter behavior that used to have a different name
class IRenamedAdapterBehavior(Interface):
    pass


@implementer(IRenamedAdapterBehavior)
class RenamedAdapterBehavior:
    def __init__(self, context):
        self.context = context


# Adapter behavior with explicit context restriction
class IRestrictedAdapterBehavior(Interface):
    pass


@implementer(IRestrictedAdapterBehavior)
class RestrictedAdapterBehavior:
    def __init__(self, context):
        self.context = context


class IMinimalContextRequirements(Interface):
    pass


# Behavior with interface and for_ implied by factory
class IImpliedRestrictionAdapterBehavior(Interface):
    pass


class ISomeContext(Interface):
    pass


@implementer(IImpliedRestrictionAdapterBehavior)
@adapter(ISomeContext)
class ImpliedRestrictionAdapterBehavior:
    def __init__(self, context):
        self.context = context


# Behavior with marker
class IMarkerBehavior(Interface):
    pass


# Behavior to be registered with name only
class INameOnlyBehavior(Interface):
    pass


# For test of the annotation factory
class IAnnotationStored(Interface):
    some_field = schema.TextLine(title="Some field", default="default value")


# Behavior and marker
class IMarkerAndAdapterBehavior(Interface):
    pass


class IMarkerAndAdapterBehavior2(Interface):
    pass


class IMarkerAndAdapterMarker(Interface):
    pass


class IMarkerAndAdapterMarker2(Interface):
    pass


class DummyBehaviorImpl:
    def __init__(self, context):
        self.context = context


def test_suite():
    return unittest.TestSuite(
        (
            doctest.DocFileSuite(
                "behaviors.rst",
                setUp=zope.component.testing.setUp,
                tearDown=zope.component.testing.tearDown,
                globs={
                    "print_function": print,
                },
            ),
            doctest.DocFileSuite(
                "directives.rst",
                setUp=zope.component.testing.setUp,
                tearDown=zope.component.testing.tearDown,
            ),
            doctest.DocFileSuite(
                "annotation.rst",
                setUp=zope.component.testing.setUp,
                tearDown=zope.component.testing.tearDown,
            ),
        )
    )
