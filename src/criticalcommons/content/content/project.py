from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage
from z3c.relationfield.schema import RelationList
from z3c.relationfield.schema import RelationChoice
from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder

from criticalcommons.content.content.lecture import ILecture

from criticalcommons.content import _

class IProject(form.Schema):
    """A project.
    """
    
    title = schema.TextLine(
            title=_(u"Title"),
        )

    summary = schema.Text(
            title=_(u"Project summary"),
        )
    
    fullDescription = RichText(
            title=_(u"Project description"),
            required=True
        )

    projectCreator = schema.TextLine(
            title=_(u"Project Creator(s)"),
        )

    projectImage = NamedImage(
            title=_(u"Project image"),
            description=_(u"Select a image to represent this project"),
            required=True,
        )

    projectImageDescription = schema.Text(
            title=_(u"Image caption"),
        )

    linkOne = schema.Text(
            title=_(u"Related URL 1"),
            description=_(u"Related URL for this project"),
            required=True,
        )

    linkTwo = schema.Text(
            title=_(u"Related URL 2"),
            description=_(u"Related URL for this project"),
            required=False,
        )

    linkThree = schema.Text(
            title=_(u"Related URL 3"),
            description=_(u"Related URL for this project"),
            required=False,
        )

    #TODO Add a proper content type restriction once we have all the content types
    form.widget(relatedProjectContent=AutocompleteFieldWidget)
    relatedProjectContent = RelationList(
            title=u"Related content.",
            description=_(u"Links to other related content for this project. Start typing to search through content."),
            default=[],
            value_type=RelationChoice(title=_(u"Related"),
                                      source=ObjPathSourceBinder(object_provides=ILecture.__identifier__)),
            required=False,
        )
