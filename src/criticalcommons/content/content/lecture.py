from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from criticalcommons.content import _

class ILecture(form.Schema):
    """A lecture.
    """
    
    summary = schema.Text(
            title=_(u"A short summary"),
        )
    
    fullDescription = RichText(
            title=_(u"Full description"),
            required=True
        )
