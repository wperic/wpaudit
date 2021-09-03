from wpaudit.providers.aws.resources.vpcs import Vpcs
from wpaudit.providers.aws.resources.ec2.instances import EC2Instances
from wpaudit.providers.aws.resources.ec2.securitygroups import SecurityGroups
from wpaudit.providers.aws.resources.ec2.networkinterfaces import NetworkInterfaces


class Ec2Vpcs(Vpcs):
    _children = [
        (EC2Instances, 'instances'),
        (SecurityGroups, 'security_groups'),
        (NetworkInterfaces, 'network_interfaces')
    ]
