from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from plumi.content.interfaces import IPlumiVideo
from Products.Archetypes.public import StringField, ReferenceField
from Products.Archetypes.public import StringWidget, ReferenceWidget
from archetypes.schemaextender.field import ExtensionField

class MyStringField(ExtensionField, StringField):
    """" just a string field """

class MyReferenceField(ExtensionField, ReferenceField):
    """ just a reference field """

class ClipExtender(object):
    """ schema extender for Plumi Videos, adds filmName & commentaries """
    adapts(IPlumiVideo)
    implements(ISchemaExtender)

    fields = [
             MyStringField("filmName", required=True, 
		widget = StringWidget(label="Name of film", description="Name of the film that the clip comes from")),
             ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


