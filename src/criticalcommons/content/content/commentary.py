from five import grok
from zope import schema

from plone.directives import form, dexterity

from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage

from criticalcommons.content import _

class ICommentary(form.Schema):
    """A commentary.
    """
    
    summary = schema.Text(
            title=_(u"A short summary"),
        )
    
    textCommentary = RichText(
            title=_(u"Text commentary"),
            required=True
        )
