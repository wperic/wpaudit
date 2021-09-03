from wpaudit.providers.aliyun.resources.base import AliyunCompositeResources
from wpaudit.providers.aliyun.resources.oss.buckets import Buckets


class OSS(AliyunCompositeResources):
    _children = [
        (Buckets, 'buckets')
    ]

    async def fetch_all(self, **kwargs):
        await self._fetch_children(resource_parent=self)
