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
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from AccessControl.SecurityManagement import newSecurityManager
from Products.CMFCore.interfaces import ISiteRoot


class ICommentary(Interface):
    title = schema.TextLine(title=_(u"Title"))
    #form.widget(FullDescription=WysiwygFieldWidget)
    body = schema.Text(title=_(u"Body"))

class CommentaryForm(form.Form):

    grok.context(ISiteRoot)
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
            self.status = _(u"The commentary has been created")
            return
        normalizer = getUtility(IIDNormalizer)
        try:
            target_folder = home.commentaries
            new_id = target_folder.invokeFactory(id=str(DateTime.DateTime().millis()), type_name='Commentary', title=title)
            obj = target_folder[new_id]
            obj.textCommentary = RichTextValue(unicode(body), 'text/html', 'text/html', 'utf-8')
            RelatedItems = self.context.getRelatedItems()
            RelatedItems.append(obj)
            self.context.setRelatedItems(RelatedItems)
            #used to save the related items
            #also add the video to the commentary's related items, to be used on the subscribers for when deleting a commentary
            self.context.reindexObject()
            wft = getToolByName(obj, 'portal_workflow')
            for state in ['submit','show','process','publish']:
                try:
                    wft.doActionFor(obj, state)
                except:
                    pass
            try:
                intid = getUtility(IIntIds).getId(self.context)
                relatedVids = [RelationValue(intid)]
                obj.relatedItems = relatedVids
            except KeyError:
                to_id = getUtility(IIntIds).register(self.context)
                relatedVids = [RelationValue(to_id)]
                obj.relatedItems = relatedVids
        except Exception as e:
            self.status = _(u"Failed to publish commentary")
            return

        wft = getToolByName(self.context, 'portal_workflow')
        state = wft.getInfoFor(self.context, 'review_state')
        try:
            if state == "private":
                try:
                    wft.doActionFor(self.context, 'show')
                except:
                    pass
                try:
                    wft.doActionFor(self.context, 'submit')
                except:
                    pass
                try:
                    wft.doActionFor(self.context, 'publish')
                except:
                    pass
        except: 
            pass

CommentaryView = wrap_form(CommentaryForm)
