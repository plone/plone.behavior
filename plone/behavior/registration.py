# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from zope.interface import implementer


@implementer(IBehavior)
class BehaviorRegistration(object):

    def __init__(self, title, description, interface, marker, factory):
        self.title = title
        self.description = description
        self.interface = interface
        self.marker = marker
        self.factory = factory

    def __repr__(self):
        return "<BehaviorRegistration for {0}>".format(
            self.interface.__identifier__
        )
