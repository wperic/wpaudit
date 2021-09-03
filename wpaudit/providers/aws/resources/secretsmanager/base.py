from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions

from .secrets import Secrets


class SecretsManager(Regions):
    _children = [
        (Secrets, 'secrets')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('sqs', facade)
