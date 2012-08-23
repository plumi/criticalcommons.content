from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder

from criticalcommons.content import _

class ILecture(form.Schema):
    """A lecture.
    """
    
    fullDescription = RichText(
            title=_(u"Lecture description"),
            required=True
        )

    form.widget(relatedItems=AutocompleteFieldWidget)
    relatedItems = RelationList(
            title=u"Clips",
            description=_(u"Select clips to create a playlist that accompanies this lecture. Start typing to search for relevant clips. You may include as many clips as you want. Clips may be added or deleted at any time."),
            default=[],
            value_type=RelationChoice(title=_(u"Related"),
                                      source=ObjPathSourceBinder(portal_types='PlumiVideo')),
                                      #source=ObjPathSourceBinder(object_provides=IPlumiVideo.__identifier__))),
            required=False,
        )
