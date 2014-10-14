# -*- coding: utf-8 -*-
from plone.behavior.interfaces import IBehavior
from zope.component import getUtilitiesFor
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary


def BehaviorsVocabularyFactory(context):
    behaviors = getUtilitiesFor(IBehavior)
    items = [(reg.title, reg.interface.__identifier__)
             for (title, reg) in behaviors]
    return SimpleVocabulary.fromItems(items)

directlyProvides(BehaviorsVocabularyFactory, IVocabularyFactory)
