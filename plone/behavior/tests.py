# -*- coding: utf-8 -*-
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
import doctest
import unittest
import zope.component.testing


# Simple adapter behavior - no context restrictions
class IAdapterBehavior(Interface):
    pass


@implementer(IAdapterBehavior)
class AdapterBehavior(object):
    def __init__(self, context):
        self.context = context


# Adapter behavior with explicit context restriction
class IRestrictedAdapterBehavior(Interface):
    pass


@implementer(IRestrictedAdapterBehavior)
class RestrictedAdapterBehavior(object):
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
class ImpliedRestrictionAdapterBehavior(object):

    def __init__(self, context):
        self.context = context


# Behavior with marker
class IMarkerBehavior(Interface):
    pass


# For test of the annotation factory
class IAnnotationStored(Interface):
    some_field = schema.TextLine(title=u"Some field", default=u"default value")


# Behavior and marker
class IMarkerAndAdapterBehavior(Interface):
    pass


class IMarkerAndAdapterMarker(Interface):
    pass


def test_suite():
    return unittest.TestSuite((

        doctest.DocFileSuite(
            'behaviors.txt',
            tearDown=zope.component.testing.tearDown
        ),
        doctest.DocFileSuite(
            'directives.txt',
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown
        ),
        doctest.DocFileSuite(
            'annotation.txt',
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown),
        )
    )
