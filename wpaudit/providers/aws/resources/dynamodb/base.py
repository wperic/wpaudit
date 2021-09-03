from wpaudit.providers.aws.facade.base import AWSFacade
from wpaudit.providers.aws.resources.regions import Regions
from .tables import Tables


class DynamoDB(Regions):
    _children = [
        (Tables, 'tables')
    ]

    def __init__(self, facade: AWSFacade):
        super(DynamoDB, self).__init__('dynamodb', facade)
