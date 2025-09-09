from plone.behavior.interfaces import ISchemaAwareFactory
from zope.annotation.interfaces import IAnnotatable
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import provider


@adapter(IAnnotatable)
class AnnotationsFactoryImpl:
    """A factory that knows how to store data in annotations.

    Each value will be stored as a primitive in the annotations under a key
    that consists of the full dotted name to the field being stored.

    This class is not sufficient as an adapter factory on its own. It must
    be initialised with the schema interface in the first place. That is the
    role of the Annotations factory below.
    """

    def __init__(self, context, schema):
        self.__dict__["schema"] = schema
        self.__dict__["prefix"] = schema.__identifier__ + "."
        self.__dict__["annotations"] = IAnnotations(context)
        alsoProvides(self, schema)

    def __getattr__(self, name):
        if name not in self.__dict__["schema"]:
            raise AttributeError(name)

        annotations = self.__dict__["annotations"]
        key_name = self.__dict__["prefix"] + name
        if key_name not in annotations:
            return self.__dict__["schema"][name].missing_value

        return annotations[key_name]

    def __setattr__(self, name, value):
        if name not in self.__dict__["schema"]:
            super().__setattr__(name, value)
        else:
            prefixed_name = self.__dict__["prefix"] + name
            self.__dict__["annotations"][prefixed_name] = value


@provider(ISchemaAwareFactory)
class AnnotationStorage:
    """Behavior adapter factory class for storing data in annotations."""

    def __init__(self, schema):
        self.schema = schema
        self.__component_adapts__ = (IAnnotatable,)

    def __call__(self, context):
        return AnnotationsFactoryImpl(context, self.schema)
