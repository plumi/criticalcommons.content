from zope import schema
from zope.interface import Interface
from z3c.form import form, field, button
from five import grok
#from plone.autoform.form import AutoExtensibleForm
#from plone.directives import form
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from criticalcommons.content import _
from plumi.content.interfaces import IPlumiVideo
from plone.z3cform.layout import wrap_form


class ICommentary(Interface):
    title = schema.TextLine(title=_(u"Title"))
    #form.widget(FullDescription=WysiwygFieldWidget)
    body = schema.Text(title=_(u"Body"))

class CommentaryForm(form.Form):
    fields = field.Fields(ICommentary)
    ignoreContext = True

    @button.buttonAndHandler(_(u'Save changes'), name='apply')
    def handleApply(self, action):
        print "inside save"
        import pdb;pdb.set_trace()

CommentaryView = wrap_form(CommentaryForm)
