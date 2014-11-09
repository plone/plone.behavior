# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from zope.interface import implementer
from zope.component import getUtility
from zope.component import ComponentLookupError


@implementer(IBehavior)
class BehaviorRegistration(object):

    def __init__(self, title, description, interface,
                 marker, factory, name=None):
        self.title = title
        self.description = description
        self.interface = interface
        self.marker = marker
        self.factory = factory
        self.name = name

    def __repr__(self):
        return "<BehaviorRegistration for {0}>".format(
            self.interface.__identifier__
        )


class BehaviorRegistrationNotFound(Exception):
    """Exception thrown if behavior registration lookup fails.
    """


def lookup_behavior_registration(name=None, identifier=None):
    """Lookup behavior registration either by name or interface identifier.

    ``ValueError`` is thrown if function call is incomplete.
    ``BehaviorRegistrationNotFound`` is thrown if lookup fails.
    """
    try:
        assert(name or identifier)
    except AssertionError:
        raise ValueError('Either ``name`` or ``identifier`` must be given')
    # identifier rules if given
    if identifier:
        name = identifier
    try:
        return getUtility(IBehavior, name=name)
    except ComponentLookupError:
        raise BehaviorRegistrationNotFound(name)
