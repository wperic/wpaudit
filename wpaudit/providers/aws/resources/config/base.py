from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.config.recorders import Recorders
from wpaudit.providers.aws.resources.config.rules import Rules
from wpaudit.providers.aws.resources.regions import Regions


class Config(Regions):
    _children = [
        (Recorders, 'recorders'),
        (Rules, 'rules')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('config', facade)
