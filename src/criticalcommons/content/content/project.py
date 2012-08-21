from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from criticalcommons.content import _

class IProject(form.Schema):
    """A project.
    """
    
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
