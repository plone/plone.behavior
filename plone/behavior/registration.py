# -*- coding: utf-8 -*-
from plone.behavior import logger
from plone.behavior.interfaces import IBehavior
from zope.component import ComponentLookupError
from zope.component import getUtilitiesFor
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
  {description}{extra_info}
>"""


@implementer(IBehavior)
class BehaviorRegistration(object):

    def __init__(self, title, description, interface,
                 marker, factory, name=None, former_dotted_names=''):
        self.title = title
        self.description = description
        self.interface = interface
        self.marker = marker
        self.factory = factory
        self.name = name
        self.former_dotted_names = former_dotted_names

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
                subsequent_indent='  ',
            ),
            'extra_info': (
                self.former_dotted_names and
                '\n  former dotted names: {0}'.format(self.former_dotted_names)
            ),
        }
        return REGISTRATION_REPR.format(**info)


class BehaviorRegistrationNotFound(Exception):
    """Exception thrown if behavior registration lookup fails.
    """


def lookup_behavior_registration(
        name=None, identifier=None, warn_about_fallback=True):
    """Look up behavior registration either by name or interface identifier.
       Fall back to checking the former_dotted_names if the lookup is not
       successful.

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
        for id_, behavior in getUtilitiesFor(IBehavior):
            # Before we raise an error, iterate over all behaviors and check
            # if the requested name is registered as a former dotted name.
            if name in behavior.former_dotted_names:
                if warn_about_fallback:
                    logger.warn(
                        'The dotted name "{0}" is deprecated. It has been '
                        'changed to "{1}"'.format(
                            name, behavior.interface.__identifier__, ))
                return behavior
        raise BehaviorRegistrationNotFound(name)
