from plone.behavior.interfaces import IBehavior
from zope.component import getUtilitiesFor
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def BehaviorsVocabularyFactory(context):
    behaviors = getUtilitiesFor(IBehavior)
    return SimpleVocabulary(
        [
            SimpleTerm(
                value=reg.interface.__identifier__,
                token=reg.name or reg.interface.__identifier__,
                title=reg.title,
            )
            for (utility_name, reg) in behaviors
            if not reg.name or reg.name == utility_name
        ]
    )
