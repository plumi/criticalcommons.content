from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CriticalcommonsContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import criticalcommons.content
        xmlconfig.file('configure.zcml',
                       criticalcommons.content,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'criticalcommons.content:default')

CRITICALCOMMONS_CONTENT_FIXTURE = CriticalcommonsContent()
CRITICALCOMMONS_CONTENT_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(CRITICALCOMMONS_CONTENT_FIXTURE, ),
                       name="CriticalcommonsContent:Integration")