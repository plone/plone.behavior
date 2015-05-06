# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from zope.component import getUtilitiesFor
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def BehaviorsVocabularyFactory(context):
    behaviors = getUtilitiesFor(IBehavior)
    items = [
        (reg.title, reg.interface.__identifier__) for (title, reg) in behaviors
    ]
    return SimpleVocabulary.fromItems(items)
