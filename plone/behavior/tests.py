# -*- coding: utf-8 -*-
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import doctest
import unittest
import zope.component.testing

import re
import sys

SKIP_PYTHON_2 = doctest.register_optionflag('SKIP_PYTHON_2')
SKIP_PYTHON_3 = doctest.register_optionflag('SKIP_PYTHON_3')
IGNORE_B = doctest.register_optionflag('IGNORE_B')
IGNORE_U = doctest.register_optionflag('IGNORE_U')


class PolyglotOutputChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if optionflags & SKIP_PYTHON_3 and sys.version_info >= (3,):
            return True
        elif optionflags & SKIP_PYTHON_2:
            return True

        if hasattr(self, '_toAscii'):
            got = self._toAscii(got)
            want = self._toAscii(want)

        # Naive fix for comparing byte strings
        if got != want and optionflags & IGNORE_B:
            got = re.sub(r'^b([\'"])', r'\1', got)
            want = re.sub(r'^b([\'"])', r'\1', want)

        # Naive fix for comparing byte strings
        if got != want and optionflags & IGNORE_U:
            got = re.sub(r'^u([\'"])', r'\1', got)
            want = re.sub(r'^u([\'"])', r'\1', want)

        return doctest.OutputChecker.check_output(
            self, want, got, optionflags)


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
            'behaviors.rst',
            tearDown=zope.component.testing.tearDown,
            checker=PolyglotOutputChecker()
        ),
        doctest.DocFileSuite(
            'directives.rst',
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown,
            checker=PolyglotOutputChecker()
        ),
        doctest.DocFileSuite(
            'annotation.rst',
            setUp=zope.component.testing.setUp,
            tearDown=zope.component.testing.tearDown,
            checker=PolyglotOutputChecker()
        ))
    )
