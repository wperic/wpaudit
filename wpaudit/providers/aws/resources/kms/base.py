from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions

from .keys import Keys


class KMS(Regions):
    _children = [
        (Keys, 'keys'),
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('kms', facade)
