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

class IClip(form.Schema):
    """ Publish clip form schema """

    form.fieldset('categorize',
                  label=u"Categorise",
                  fields=['Genre', 'Country', 'Topics', 'Tags',
                          'Director', 'Producer', 'Email', 'Organisation',
                          'ProductionCompany']
                  )

    Title = schema.TextLine(title=_(u"Title"),
                            max_length=160,
                            required=True,
                            )

    Description = schema.Text(title=_(u"Media Description"),
                              required=True,
                              description=_(u"Briefly describe the media and its critical context."),
                              )

    DateProduced = schema.TextLine(title=_(u"Year Produced"),
                               required=True,
                               description=_(u"The year this media was originally created."),
                               constraint=validate_date,
                               )

    FilmName = schema.TextLine(title=_(u"Name of original media"), description=_(u"What is the title of the work this media comes from?"))

    Tags = schema.TextLine(title=_(u"Tags"),
                           description=_(u"Separate tags with commas, e.g., race, class, gender, editing, lighting, framing, etc."),
                           required=False,
                           )

    Director = schema.TextLine(title=_(u"Filmmaker/Creator"),
                               required=True,
                               )

    Distributor = schema.TextLine(title=_(u"Media Distributor"),
                               description=_(u"Where (or from whom) is the original media available?"),
                               required=False,
                               )

    Genre = schema.Choice(title=_(u"Genre"),
                          required=False,
                          source=get_video_genres,
                          default='none',
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

    #FIX: find a more native validation -eg provided by zope.schema
    Thumbnail = schema.Bytes(title=u'Add thumbnail',
                             constraint=validate_image,
                             description=u"We will automatically generate an image, but you may prefer to upload your own",
                             required=False,
                             )

def newcreate_object(self, context, data, uid, subject):
    context.invokeFactory('PlumiVideo', id=uid,
                           description=data['Description'],
                           DateProduced=data['DateProduced'],
                           thumbnailImage=data['Thumbnail'],
                           Genre=data['Genre'],
                           Countries=data['Country'],
                           Categories=data['Topics'],
                           subject=subject,
                           Director=data['Director'] or '',
                           Distributor=data['Distributor'] or '',
                           FilmName=data['FilmName'] or '',
                           )


def newUpdateWidgets(self):
    super(VideoAddForm, self).updateWidgets()

from plumi.content.browser.forms import VideoAddForm
VideoAddForm.schema = IClip
VideoAddForm.updateWidgets = newUpdateWidgets
VideoAddForm.create_object = newcreate_object
VideoAddForm.label = u"Share Media"
