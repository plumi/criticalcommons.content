from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder


from criticalcommons.content import _

class ICommentary(form.Schema):
    """A commentary.
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
        )

    summary = schema.Text(
            title=_(u"Commentary summary"),
        )
    
    commentary = RichText(
            title=_(u"Commentary"),
            required=True
        )

    form.widget(relatedItems=AutocompleteFieldWidget)
    relatedItems = RelationList(
            title=u"Clips",
            description=_(u"Start typing in the field below to search for clips to which this commentary should be linked."),
            default=[],
            value_type=RelationChoice(title=_(u"Related"),
                                      source=ObjPathSourceBinder()),
            required=False,
        )
