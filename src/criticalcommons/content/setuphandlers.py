import logging
from Products.CMFCore.utils import getToolByName
from criticalcommons.content.vocabs  import vocab_set as vocabs
from criticalcommons.content.config import TOPLEVEL_TAXONOMY_FOLDER , GENRE_FOLDER, CATEGORIES_FOLDER, COUNTRIES_FOLDER
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from plumi.app.translations import createTranslations, deleteTranslations

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("plumi")

def publishObject(wftool,obj):
    logger=logging.getLogger('plumi.app')
    try:
        logger.info('publishing %s ' % obj)
        wftool.doActionFor(obj,action='publish')
    except WorkflowException:
        logger.error('caught workflow exception!') 
        pass

def setupVocabs(portal, logger):
    #
    #ATVocabManager setup
    #
    logger.info('Starting ATVocabManager configuration ')
    atvm = getToolByName(portal, ATVOCABULARYTOOL)
    wftool = getToolByName(portal,'portal_workflow')

    for vkey in vocabs.keys():
        # create vocabulary if it doesnt exist:
        vocabname = vkey
        if atvm.getVocabularyByName(vocabname):
            atvm.manage_delObjects(vocabname)
        logger.debug("adding vocabulary %s" % vocabname)
        atvm.invokeFactory('SimpleVocabulary', vocabname)

        vocab = atvm[vocabname]

        #delete the 'default' item
        if hasattr(vocab, 'default'):
            vocab.manage_delObjects(['default'])

        for (ikey, value) in vocabs [vkey]:
            if not hasattr(vocab, ikey):
                vocab.invokeFactory('SimpleVocabularyTerm', ikey)
                logger.debug("adding vocabulary item %s %s" % (ikey,value))
                vocab[ikey].setTitle(value)

        #reindex
        vocab.reindexObject()

def setupDocuments(self, logger):
    
    wftool = getToolByName(self,'portal_workflow')

    #Avoid doing all the following when reinstalling

    # Taxonomy - smart folder hierarchy setup - genres/categories/countries/ 
    #    for videos we automatically [RE]create collections , hierarchically, 
    #    for all available vocabulary items
    #
    logger.info('starting taxonomy hierarchy setup')

    #delete the taxonomy folder and it's translations.
    #this should also delete all children and children's children etc
    try:
        canon = getattr(self, 'taxonomy')
        deleteTranslations(canon)
        self.manage_delObjects(['taxonomy'])
    except:
        pass
    self.invokeFactory('Folder', id = TOPLEVEL_TAXONOMY_FOLDER,
                       title = _(u'Browse Content'),
#                      description = _(u'The top-level taxonomy of the content')
                       )
    taxonomy_fldr = getattr(self,TOPLEVEL_TAXONOMY_FOLDER,None) 
    # we start in 'taxonomy', and shld already have sub-folders constructed
    #    to hold the topics objects (smart folders), via generic setup XML
    publishObject(wftool,taxonomy_fldr)

    createTranslations(self,taxonomy_fldr)
    layout_name = "video_listing_view"


    #
    # 1 of 5: video genre
    #
    taxonomy_fldr.invokeFactory('Folder', id=GENRE_FOLDER, 
                                title=_(u'Media Genres'))
    genre_fldr = getattr(taxonomy_fldr, GENRE_FOLDER,None)
    publishObject(wftool,genre_fldr)
    createTranslations(self,genre_fldr)
    #description string for new smart folders
    for vocab in vocabs['video_genre']:
        new_smart_fldr_id = vocab[0]

        #skip topic creation if id=None
        if not new_smart_fldr_id == "none":
            #make the new SmartFolder
            genre_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1])
            fldr = getattr(genre_fldr,new_smart_fldr_id)
             
            # Filter results to Plumi Video
            type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
            #Have to use the name of the Title of the Type you want to filter.
            type_criterion.setValue("Video")
             
            # Filter results to this individual genre
            type_criterion = fldr.addCriterion('getGenre', 'ATSimpleStringCriterion' )
            #match against the ID of the vocab term. see getGenre in content types 
            type_criterion.setValue(vocab[0])
            ## add criteria for showing only published videos
            state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
            state_crit.setValue(['published','featured'])
            
            #XXX used to have a custom getFirstPublishedTransitionTime 
            #sort on reverse date order, using the first published time transition
            sort_crit = fldr.addCriterion('effective',"ATSortCriterion")
            sort_crit.setReversed(True)

            #make the folder published
            fldr.setLayout(layout_name)
            publishObject(wftool,fldr)
            createTranslations(self,fldr)

    #
    # 2 of 5: video categories aka topic
    #
    taxonomy_fldr.invokeFactory('Folder',id=CATEGORIES_FOLDER,
                                title=_(u'Media Topics'))
    categ_fldr = getattr(taxonomy_fldr, CATEGORIES_FOLDER,None)
    publishObject(wftool,categ_fldr)
    createTranslations(self,categ_fldr)

    for vocab in vocabs['video_categories']:
        new_smart_fldr_id = vocab[0]
        #skip topic creation if id=None
        if not new_smart_fldr_id == "none":
            #make the new SmartFolder
            categ_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=vocab[1])
            fldr = getattr(categ_fldr,new_smart_fldr_id)

            # Filter results to Plumi Video
            type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
            type_criterion.setValue("Video")
            # Filter results to this individual category
            type_criterion = fldr.addCriterion('getCategories', 'ATListCriterion' )
            #match against the ID of the vocab term. see getCategories in content objects
            type_criterion.setValue(vocab[0])
            #match if any vocab term is present in the video's selected categories
            type_criterion.setOperator('or')
            ## add criteria for showing only published videos
            state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
            state_crit.setValue(['published','featured'])
            #sort on reverse date order
            #XXX old getfirstpublishedtransition time 
            sort_crit = fldr.addCriterion('effective',"ATSortCriterion")
            sort_crit.setReversed(True)

            #make the folder published.
            fldr.setLayout(layout_name)
            publishObject(wftool,fldr)
            createTranslations(self,fldr)


    #
    # 3 of 5: video countries
    #
   
    #Countries
    #get the countries from the country vocab!

    taxonomy_fldr.invokeFactory('Folder',id=COUNTRIES_FOLDER,
                                title=_(u'Countries'))
    countries_fldr = getattr(taxonomy_fldr,COUNTRIES_FOLDER,None)
    publishObject(wftool,countries_fldr)
    createTranslations(self,countries_fldr)

    for country in vocabs['video_countries']:
        new_smart_fldr_id = country[0]

        # maybe it already exists?
        try: 
            #skip topic creation if id=None
            if not new_smart_fldr_id == "none":
                # make the new SmartFolder              
                if new_smart_fldr_id == 'XX':
                    #International country has --International-- title to show first on drop down, we're overriding that
                    countries_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title='International') 
                else:
                    countries_fldr.invokeFactory('Topic', id=new_smart_fldr_id,title=country[1]) 
                fldr = getattr(countries_fldr,new_smart_fldr_id)

                # Filter results to  Plumi Video
                type_criterion = fldr.addCriterion('Type', 'ATPortalTypeCriterion' )
                type_criterion.setValue("Video")

                # Filter results to this individual category
                type_criterion = fldr.addCriterion('getCountries', 'ATListCriterion' )
                #
                #match against the ID of the vocab term. see getCategories in content objects
                type_criterion.setValue(country[0])
                #match if any vocab term is present in the video's selected categories
                type_criterion.setOperator('or')
                ## add criteria for showing only published videos
                state_crit = fldr.addCriterion('review_state', 'ATListCriterion')
                state_crit.setValue(['published','featured'])
                #sort on reverse date order
                sort_crit = fldr.addCriterion('effective',"ATSortCriterion")
                sort_crit.setReversed(True)
                #publish folder
                fldr.setLayout(layout_name)
                publishObject(wftool,fldr)
                createTranslations(self,fldr)
        except:
            # should be ok from previous installation
            pass


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('CC.content_various.txt') is None:
        return

    portal = context.getSite()
    logger = logging.getLogger('plumi.app')
    setupVocabs(portal, logger)
    setupDocuments(portal, logger)

