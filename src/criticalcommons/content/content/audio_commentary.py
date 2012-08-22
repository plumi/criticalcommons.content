from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedFile
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder

from criticalcommons.content import _

class IAudioCommentary(form.Schema):
    """A commentary.
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
        )

    summary = schema.Text(
            title=_(u"A short summary"),
        )
    
    textCommentary = RichText(
            title=_(u"Text commentary"),
            required=True
        )

    audioCommentary = NamedFile(
            title=_(u"Audio commentary"),
            required=True
        )

    form.widget(relatedClips=AutocompleteFieldWidget)
    relatedClips = RelationList(
            title=u"Clips",
            description=_(u"Start typing in the field below to search for clips to which this commentary should be linked."),
            default=[],
            value_type=RelationChoice(title=_(u"Related"),
                                      source=ObjPathSourceBinder()),
            required=False,
        )
