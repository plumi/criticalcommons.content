from zope.lifecycleevent.interfaces import  IObjectModifiedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from Products.CMFCore.utils import getToolByName
from criticalcommons.content.content.commentary import ICommentary
from zope.component import adapter
from plumi.content.interfaces.plumivideo import IPlumiVideo
from Products.Archetypes.interfaces import IObjectInitializedEvent, IObjectEditedEvent
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from zope.component import getUtility


def removeCommentary(obj, event):
    try:
        for item in obj.relatedItems:
            video = item.to_object
            rel = video.getRelatedItems()
            # remove obj from related video's relatedItems field
            for r in rel:
                if r == obj:
                    rel.remove(r)
                    video.setRelatedItems(rel)
                    video.reindexObject()

            # if no other commentaries in video make video private
            relCom = [r for r in rel if r.portal_type=='Commentary']
            if not len(relCom):
                wft = getToolByName(video, 'portal_workflow')
                review_state = wft.getInfoFor(video, 'review_state')
                if review_state == 'featured':
                    wft.doActionFor(video, 'unfeature')
                    review_state = wft.getInfoFor(video, 'review_state')
                if review_state == 'published':
                    wft.doActionFor(video, 'retract')
                    wft.doActionFor(video, 'hide')
                elif review_state == 'pending':
                    wft.doActionFor(video, 'hide')
    except:
        pass      

def modifyCommentary(obj, event):
    try:
        for item in obj.relatedItems:
            video = item.to_object
            rel = video.getRelatedItems()
            exists = len([r for r in rel if r == obj])
            if not exists:
                rel.append(obj)
            video.setRelatedItems(rel)
            video.reindexObject()
            try:
                #publish the video, if it is private
                wft = getToolByName(video, 'portal_workflow')
                state = wft.getInfoFor(video, 'review_state')
                if state == "private":
                    try:
                        wft.doActionFor(video, 'show')
                    except:
                        pass
                    try:
                        wft.doActionFor(video, 'submit')
                    except:
                        pass
                    try:
                        wft.doActionFor(video, 'publish')
                    except:
                        pass
            except:
                pass
    except:
        pass
def modifyPlumiVideo(obj, event):
    'when editing a Video, check if there are commentaries added, and associate the Video with them'
    commentaries = [i for i in obj.getRelatedItems() if i.portal_type == 'Commentary']
    for commentary in commentaries:
        rel = commentary.relatedItems
        exists = []
        for r in rel: #check related videos, if obj exists skip, otherwise add it
            v = r.to_object
            if v == obj:
                exists.append(v)
        if not exists:
            intid = getUtility(IIntIds).getId(obj)
            relatedVids = [RelationValue(intid)] + rel
            commentary.relatedItems = relatedVids

