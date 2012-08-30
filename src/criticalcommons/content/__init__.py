# -*- extra stuff goes here -*-

from zope.i18nmessageid import MessageFactory

import criticalcommons.content.patch

_ = MessageFactory("criticalcommons.content")

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
