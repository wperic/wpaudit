from wpaudit.providers.aws.resources.vpcs import Vpcs
from wpaudit.providers.aws.resources.elasticache.cluster import Clusters
from wpaudit.providers.aws.resources.elasticache.subnetgroups import SubnetGroups


class ElastiCacheVpcs(Vpcs):
    _children = [
        (Clusters, 'clusters'),
        (SubnetGroups, 'subnet_groups')
    ]
