from wpaudit.providers.aliyun.facade.base import AliyunFacade
from wpaudit.providers.base.services import BaseServicesConfig
from wpaudit.providers.aliyun.resources.ram.base import RAM
from wpaudit.providers.aliyun.resources.actiontrail.base import ActionTrail
from wpaudit.providers.aliyun.resources.vpc.base import VPC
from wpaudit.providers.aliyun.resources.ecs.base import ECS
from wpaudit.providers.aliyun.resources.rds.base import RDS
from wpaudit.providers.aliyun.resources.kms.base import KMS
from wpaudit.providers.aliyun.resources.oss.base import OSS



class AliyunServicesConfig(BaseServicesConfig):
    def __init__(self, credentials, **kwargs):
        super().__init__(credentials)

        facade = AliyunFacade(credentials)

        self.actiontrail = ActionTrail(facade)
        self.ram = RAM(facade)
        self.ecs = ECS(facade)
        self.rds = RDS(facade)
        self.vpc = VPC(facade)
        self.kms = KMS(facade)
        self.oss = OSS(facade)

    def _is_provider(self, provider_name):
        return provider_name == 'aliyun'
