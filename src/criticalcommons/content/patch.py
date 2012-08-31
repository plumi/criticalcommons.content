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
                  fields=['Genre', 'Country', 'Topics', 'Tags', 'Location',
                          'Director', 'Producer', 'Email', 'Organisation',
                          'ProductionCompany', 'Website']
                  )

    Title = schema.TextLine(title=_(u"Title"),
                            max_length=160,
                            required=True,
                            )

    Description = schema.Text(title=_(u"Short summary"),
                              required=True,
                              max_length=160,
                              description=_(u"Describe your video in 160 characters."),
                              )

    DateProduced = schema.Date(title=_(u"Date Produced"),
                               required=True,
                               description=_(u"The date the video content was released."),
                               )

    form.widget(FullDescription=WysiwygFieldWidget)
    FullDescription = schema.Text(title=_(u"Full Description"),
                                  required=False,
                                  )

    #FIX: find a more native validation -eg provided by zope.schema
    Thumbnail = schema.Bytes(title=u'Add thumbnail',
                             constraint=validate_image,
                             description=u"We will automatically generate an image, but you may prefer to upload your own",
                             required=False,
                             )

    Genre = schema.Choice(title=_(u"Genre"),
                          required=False,
                          source=get_video_genres,
                          default='none',
                          )

    Country = schema.Choice(title=_(u"Country"),
                            required=False,
                            default='XX',
                            source=get_video_countries
                            )

    FilmName = schema.TextLine(title=_(u"Name of original media"), description=_(u"Name of the film that the clip comes from"))

    Location = schema.TextLine(title=_(u"Location"),
                               description=_(u"e.g. City or Region."),
                               required=False,
                               )

    Topics = schema.List(title=_(u"Topics"),
                         required=False,
                         description=_(u"Select topics and click arrows to add or remove"),
                         value_type=schema.Choice(source=get_video_categories),
                         default=[],
                         )

    Tags = schema.TextLine(title=_(u"Tags"),
                           description=_(u"Seperate with comma. Eg tag1, tag2, tag4"),
                           required=False,
                           )

    Director = schema.TextLine(title=_(u"Director"),
                               required=False,
                               )

    Producer = schema.TextLine(title=_(u"Producer"),
                               required=False,
                               )

    Email = schema.TextLine(title=_(u"Email Address"),
                            required=False,
                            constraint=validate_address,
                            )

    Organisation = schema.TextLine(title=_(u"Project Name"),
                                   required=False,
                                   )

    ProductionCompany = schema.TextLine(title=_(u"Production Company"),
                                        required=False,
                                        )

    Website = schema.TextLine(title=_(u"Website URL"),
                         required=False,
                         constraint=validate_URI,
                         )


def newUpdateWidgets(self):
    super(VideoAddForm, self).updateWidgets()

from plumi.content.browser.forms import VideoAddForm
VideoAddForm.schema = IClip
VideoAddForm.updateWidgets = newUpdateWidgets
