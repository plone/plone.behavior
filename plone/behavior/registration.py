# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from zope.component import ComponentLookupError
from zope.component import getUtility
from zope.interface import implementer

import sys
import textwrap


if sys.version_info[0] >= 3:
    text_type = str
else:
    text_type = unicode


REGISTRATION_REPR = """\
<{class} {name} at {id}
  schema: {identifier}
  marker: {marker}
  factory: {factory}
  title: {title}
  {description}
>"""


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
        if self.marker is not None:
            marker_info = self.marker.__identifier__
        elif self.marker is not None and self.marker is not self.interface:
            marker_info = '(uses schema as marker)'
        else:
            marker_info = '(no marker is set)'
        info = {
            'class': self.__class__.__name__,
            'id': id(self),
            'name': self.name or '(unique name not set)',
            'identifier': self.interface.__identifier__,
            'marker': marker_info,
            'factory': text_type(self.factory),
            'title': self.title or '(no title)',
            'description': textwrap.fill(
                self.description or '(no description)',
                subsequent_indent='  '
            )
        }
        return REGISTRATION_REPR.format(**info)


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
