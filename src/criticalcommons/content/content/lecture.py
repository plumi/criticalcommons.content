from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedImage
from plumi.content.interfaces.plumivideo import IPlumiVideo
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.formwidget.query.widget import QuerySourceFieldCheckboxWidget 
from criticalcommons.content import _



class ILecture(form.Schema):
    """A lecture.
    """
    
    fullDescription = RichText(
            title=_(u"Lecture text"),
            description=_(u"The text of your lecture"),
            required=True
        )

    form.widget(relatedItems=QuerySourceFieldCheckboxWidget) 
    #form.widget(relatedItems=AutocompleteMultiFieldWidget)
    relatedItems = RelationList( 
            title=u"Clips",
            description=_(u"Type keywords to select media to accompany this lecture."),
            default=[],
            value_type=RelationChoice(title=_(u"Related"), 
                       source=ObjPathSourceBinder(object_provides=IPlumiVideo.__identifier__)),
            required=True,
       )

    thumbnailImage = NamedImage(
            title=_(u"Lecture Thumbnail"),
            required=True,
            description=_(u"The thumbnail image for the lecture"),
        )

