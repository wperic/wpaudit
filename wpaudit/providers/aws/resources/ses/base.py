from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions

from .identities import Identities


class SES(Regions):
    _children = [
        (Identities, 'identities')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('ses', facade)
