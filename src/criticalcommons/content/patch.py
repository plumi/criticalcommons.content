from plumi.content.adapters import PlumiWorkflowAdapter

def newAutoPublishOrHide(self):
    return True

PlumiWorkflowAdapter.autoPublishOrHide = newAutoPublishOrHide

from zope import schema
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.directives import form
from plumi.content import plumiMessageFactory as _
from plumi.content.browser.forms import get_video_genres, get_video_categories, get_video_countries
from plumi.content.browser.forms import validate_image, validate_URI, validate_date, validate_address


class InvalidDescription(schema.ValidationError):
    __doc__ =  "Your media description is getting a little long. Please enter your critical commentary on the next page after uploading."


def validatedescription(value):
    if len(value)>=250:
        raise InvalidDescription
    return True

class IClip(form.Schema):
    """ Publish clip form schema """

#    form.fieldset('categorize',
#                  label=u"Categorise",
#                  fields=['Genre', 'Tags',
#                          'Director', 'Producer', 'Email', 'Organisation',
#                          'ProductionCompany']
#                  )

    Title = schema.TextLine(title=_(u"Title"),
                            max_length=160,
                            required=True,
                            description=_(u"Please provide a title for your contribution to Critical Commons."),
                            )

    Description = schema.Text(title=_(u"Media Description"),
                              required=True,
                              max_length=250,
                              constraint=validatedescription, 
                              description=_(u"Briefly describe the media in 250 characters."),
                              )

    #FIX: find a more native validation -eg provided by zope.schema
    Thumbnail = schema.Bytes(title=u'Add thumbnail',
                             constraint=validate_image,
                             description=u"We will automatically generate an image, but you may prefer to upload your own",
                             required=False,
                             )

    filmName = schema.TextLine(title=_(u"Name of original media"), required=True, description=_(u"What is the title of the work this media comes from?"))

    Director = schema.TextLine(title=_(u"Filmmaker/Creator"),
                               required=True,
                               )

    DateProduced = schema.TextLine(title=_(u"Year Produced"),
                               required=True,
                               description=_(u"The year this media was originally created."),
                               constraint=validate_date,
                               )

    Tags = schema.TextLine(title=_(u"Tags"),
                           description=_(u"Separate tags with commas, e.g., race, class, gender, editing, lighting, framing, etc."),
                           required=False,
                           )


    Genre = schema.Choice(title=_(u"Genre"),
                          required=False,
                          source=get_video_genres,
                          default='none',
                          )

    Distributor = schema.TextLine(title=_(u"Media Distributor"),
                               description=_(u"Where (or from whom) is the original media available?"),
                               required=False,
                               )

    Country = schema.Choice(title=_(u"Country"),
                            required=False,
                            default='US',
                            source=get_video_countries
                            )

    Topics = schema.List(title=_(u"Topics"),
                         required=False,
                         description=_(u"Select topics and click arrows to add or remove"),
                         value_type=schema.Choice(source=get_video_categories),
                         default=[],
                         )


    CommentaryTitle = schema.TextLine(title=_(u"Commentary Title"),
                            max_length=160,
                            required=False,
                            )

    CommentaryDescription = schema.Text(title=_(u"Commentary"),
                              required=False,
                              max_length=560,
                              description=_(u"You must associate commentary with your media in order for it to be publically available."),
                              )


def newcreate_object(self, context, data, uid, subject):
    context.invokeFactory('PlumiVideo', id=uid,
                           description=data['Description'],
                           DateProduced=data['DateProduced'],
                           filmName=data['filmName'] or '',
                           thumbnailImage=data['Thumbnail'],
                           Genre=data['Genre'],
                           Countries=data['Country'],
                           Categories=data['Topics'],
                           subject=data['Tags'] and data['Tags'].split(',') or '',
                           Director=data['Director'] or '',
                           Distributor=data['Distributor'] or '',
                           CommentaryTitle=data['CommentaryTitle'] or '',
                           CommentaryDescription=data['CommentaryDescription'] or ''
                           )


def newUpdateWidgets(self):
    super(VideoAddForm, self).updateWidgets()

from plumi.content.browser.forms import VideoAddForm
VideoAddForm.schema = IClip
VideoAddForm.updateWidgets = newUpdateWidgets
VideoAddForm.create_object = newcreate_object
VideoAddForm.label = u"Share Media"


def scalarnewUpdateWidgets(self):
    super(ScalarVideoAddForm, self).updateWidgets()

from plumi.content.browser.forms import ScalarVideoAddForm
ScalarVideoAddForm.schema = IClip
ScalarVideoAddForm.updateWidgets = scalarnewUpdateWidgets
ScalarVideoAddForm.create_object = newcreate_object
ScalarVideoAddForm.label = u"Upload to Critical Commons"

