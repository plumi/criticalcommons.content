from zope.lifecycleevent.interfaces import  IObjectModifiedEvent
from zope.app.container.interfaces import IObjectRemovedEvent
from Products.CMFCore.utils import getToolByName
from criticalcommons.content.content.commentary import ICommentary

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
    for item in obj.relatedItems:
        video = item.to_object
        rel = video.getRelatedItems()
        exists = len([r for r in rel if r == obj])
        if not exists:
            rel.append(obj)
        video.setRelatedItems(rel)
        try:
            #publish the video, if it is private
            wft = getToolByName(video, 'portal_workflow')
            state = wft.getInfoFor(video, 'review_state')
            if state == "private":
                wft.doActionFor(video, 'show')
                wft.doActionFor(video, 'submit')
                wft.doActionFor(video, 'publish')
        except:
            pass
