from wpaudit.providers.aliyun.facade.base import AliyunFacade
from wpaudit.providers.aliyun.resources.regions import Regions
from wpaudit.providers.aliyun.resources.ecs.instances import Instances


class ECS(Regions):
    _children = [
        (Instances, 'instances')
    ]

    def __init__(self, facade: AliyunFacade):
        super().__init__('ecs', facade)
