from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions

from .connections import Connections


class DirectConnect(Regions):
    _children = [
        (Connections, 'connections')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('directconnect', facade)
