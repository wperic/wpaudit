from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions

from .queues import Queues


class SQS(Regions):
    _children = [
        (Queues, 'queues')
    ]

    def __init__(self, facade: AWSFacade):
        super().__init__('sqs', facade)
