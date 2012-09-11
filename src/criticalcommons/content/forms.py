import DateTime
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
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.app.textfield.value import RichTextValue


class ICommentary(Interface):
    title = schema.TextLine(title=_(u"Title"))
    #form.widget(FullDescription=WysiwygFieldWidget)
    body = schema.Text(title=_(u"Body"))

class CommentaryForm(form.Form):
    fields = field.Fields(ICommentary)
    ignoreContext = True

    @button.buttonAndHandler(_(u'Save changes'), name='apply')
    def handleApply(self, action):
        pm = getToolByName(self.context, 'portal_membership')
        home = pm.getHomeFolder()
        if not home: 
            return
        title = self.request['form.widgets.title']
        body = self.request['form.widgets.body']
        existing = [i for i in self.context.getRelatedItems() if i.portal_type=='Commentary']
        dupes = [d for d in existing if d.Title() == title]
        if len(dupes):
            self.status = _(u"A commentary with the same title already exists")
            return
        normalizer = getUtility(IIDNormalizer)
        try:
            target_folder = home.commentaries
            new_id = target_folder.invokeFactory(id=str(DateTime.DateTime().millis()), type_name='Commentary', title=title)
            obj = target_folder[new_id]
            obj.textCommentary = RichTextValue(unicode(body), 'text/html', 'text/html', 'utf-8')
            self.context.setRelatedItems(self.context.getRelatedItems() + [obj])
        except Exception as e:
            self.status = _(u"Failed to publish commentary")
            print e
            return

        wft = getToolByName(self.context, 'portal_workflow')
        state = wft.getInfoFor(self.context, 'review_state')
        if state == "private":
            wft.doActionFor(self.context, 'submit')

CommentaryView = wrap_form(CommentaryForm)
