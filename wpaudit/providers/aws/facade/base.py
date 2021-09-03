from boto3.session import Session

from wpaudit.providers.aws.facade.acm import AcmFacade
from wpaudit.providers.aws.facade.awslambda import LambdaFacade
from wpaudit.providers.aws.facade.basefacade import AWSBaseFacade
from wpaudit.providers.aws.facade.cloudformation import CloudFormation
from wpaudit.providers.aws.facade.cloudtrail import CloudTrailFacade
from wpaudit.providers.aws.facade.cloudwatch import CloudWatch
from wpaudit.providers.aws.facade.config import ConfigFacade
from wpaudit.providers.aws.facade.directconnect import DirectConnectFacade
from wpaudit.providers.aws.facade.dynamodb import DynamoDBFacade
from wpaudit.providers.aws.facade.ec2 import EC2Facade
from wpaudit.providers.aws.facade.efs import EFSFacade
from wpaudit.providers.aws.facade.elasticache import ElastiCacheFacade
from wpaudit.providers.aws.facade.elb import ELBFacade
from wpaudit.providers.aws.facade.elbv2 import ELBv2Facade
from wpaudit.providers.aws.facade.emr import EMRFacade
from wpaudit.providers.aws.facade.iam import IAMFacade
from wpaudit.providers.aws.facade.kms import KMSFacade
from wpaudit.providers.aws.facade.rds import RDSFacade
from wpaudit.providers.aws.facade.redshift import RedshiftFacade
from wpaudit.providers.aws.facade.route53 import Route53Facade
from wpaudit.providers.aws.facade.s3 import S3Facade
from wpaudit.providers.aws.facade.ses import SESFacade
from wpaudit.providers.aws.facade.sns import SNSFacade
from wpaudit.providers.aws.facade.sqs import SQSFacade
from wpaudit.providers.aws.facade.secretsmanager import SecretsManagerFacade
from wpaudit.providers.aws.utils import get_aws_account_id
from wpaudit.providers.utils import run_concurrently

from wpaudit.core.conditions import print_error

# Try to import proprietary facades
try:
    from wpaudit.providers.aws.facade.cognito_private import CognitoFacade
except ImportError:
    pass
try:
    from wpaudit.providers.aws.facade.docdb_private import DocDBFacade
except ImportError:
    pass
try:
    from wpaudit.providers.aws.facade.ecs_private import ECSFacade
except ImportError:
    pass
try:
    from wpaudit.providers.aws.facade.ecr_private import ECRFacade
except ImportError:
    pass
try:
    from wpaudit.providers.aws.facade.eks_private import EKSFacade
except ImportError:
    pass
try:
    from wpaudit.providers.aws.facade.guardduty_private import GuardDutyFacade
except ImportError:
    pass


class AWSFacade(AWSBaseFacade):
    def __init__(self, credentials=None):
        super().__init__()
        self.owner_id = get_aws_account_id(credentials.session)
        self.session = credentials.session
        self._instantiate_facades()

    async def build_region_list(self, service: str, chosen_regions=None, excluded_regions=None, partition_name='aws'):

        available_services = None
        try:
            available_services = await run_concurrently(
                lambda: Session(region_name='us-east-1').get_available_services())
        except Exception as e:
            # see https://github.com/wperic/wpaudit/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                available_services = await run_concurrently(
                    lambda: Session(region_name=self.session.region_name).get_available_services())
            except Exception as e:
                # see https://github.com/wperic/wpaudit/issues/685
                # If above failed, and regions were explicitly specified, will try with those until one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            available_services = await run_concurrently(
                                lambda: Session(region_name=region).get_available_services())
                            break
                        except Exception as e:
                            exception = e
                    if not available_services:
                        raise exception
                else:
                    raise e

        if service not in available_services:
            # the cognito service is a composition of two boto3 services
            if service == "cognito":
                if "cognito-idp" not in available_services:
                    raise Exception('Service cognito-idp is not available.')
                elif "cognito-identity" not in available_services:
                    raise Exception('Service cognito-identity is not available.')
            else:
                raise Exception('Service ' + service + ' is not available.')

        regions = None
        try:
            # the cognito service is a composition of two boto3 services
            if service != "cognito":
                regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions(service,
                                                                                   partition_name))
            else:
                idp_regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions("cognito-idp",
                                                                                   partition_name))
                identity_regions = await run_concurrently(
                    lambda: Session(region_name='us-east-1').get_available_regions("cognito-identity",
                                                                                   partition_name))
                regions = [value for value in idp_regions if value in identity_regions]
        except Exception as e:
            # see https://github.com/wperic/wpaudit/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                # the cognito service is a composition of two boto3 services
                if service != "cognito":
                    regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions(service,
                                                                                                    partition_name))
                else:
                    idp_regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions("cognito-idp",
                                                                                                    partition_name))
                    identity_regions = await run_concurrently(
                        lambda: Session(region_name=self.session.region_name).get_available_regions("cognito-identity",
                                                                                                    partition_name))
                    regions = [value for value in idp_regions if value in identity_regions]
            except Exception as e:
                # see https://github.com/wperic/wpaudit/issues/685
                # If above failed, and regions were explicitly specified, will try with those until one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            # the cognito service is a composition of two boto3 services
                            if service != "cognito":
                                regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(service,
                                                                                              partition_name))
                            else:
                                idp_regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(
                                        "cognito-idp",
                                        partition_name))
                                identity_regions = await run_concurrently(
                                    lambda: Session(region_name=region).get_available_regions(
                                        "cognito-identity",
                                        partition_name))
                                regions = [value for value in idp_regions if value in identity_regions]
                            break
                        except Exception as e:
                            exception = e
                    if not regions:
                        raise exception
                else:
                    raise e

        if not regions:
            # Could be an instance of https://github.com/boto/boto3/issues/1662
            if service == 'eks':  # TODO fix when the issue is resolved
                regions = ['ap-east-1',
                           'ap-northeast-1',
                           'ap-northeast-2',
                           'ap-south-1',
                           'ap-southeast-1',
                           'ap-southeast-2',
                           'ca-central-1',
                           'eu-central-1',
                           'eu-north-1',
                           'eu-west-1',
                           'eu-west-2',
                           'eu-west-3',
                           'me-south-1',
                           'sa-east-1',
                           'us-east-1',
                           'us-east-2',
                           # 'us-west-1',
                           'us-west-2']
            else:
                print_error('"get_available_regions" returned an empty array for service "{}", '
                            'something is wrong'.format(service))

        # identify regions that are not opted-in
        ec2_not_opted_in_regions = None
        try:
            ec2_not_opted_in_regions = self.session.client('ec2', 'us-east-1') \
                .describe_regions(AllRegions=True, Filters=[{'Name': 'opt-in-status', 'Values': ['not-opted-in']}])
        except Exception as e:
            # see https://github.com/wperic/wpaudit/issues/548
            # If failed with the us-east-1 region, we'll try to use the region from the profile
            try:
                ec2_not_opted_in_regions = \
                    self.session.client('ec2', self.session.region_name). \
                        describe_regions(AllRegions=True,
                                         Filters=[{'Name': 'opt-in-status',
                                                   'Values': ['not-opted-in']}])
            except Exception as e:
                # see https://github.com/wperic/wpaudit/issues/685
                # If above failed, and regions were explicitly specified, will try with those until
                # one works
                if chosen_regions:
                    for region in chosen_regions:
                        try:
                            ec2_not_opted_in_regions = self.session.client('ec2', region).describe_regions(
                                AllRegions=True,
                                Filters=[{'Name': 'opt-in-status',
                                          'Values': ['not-opted-in']}])
                            break
                        except Exception as e:
                            exception = e
                    if not ec2_not_opted_in_regions:
                        raise exception
                else:
                    raise e

        not_opted_in_regions = []
        if ec2_not_opted_in_regions['Regions']:
            for r in ec2_not_opted_in_regions['Regions']:
                not_opted_in_regions.append(r['RegionName'])

        # include specific regions
        if chosen_regions:
            regions = [r for r in regions if r in chosen_regions]
        # exclude specific regions
        if excluded_regions:
            regions = [r for r in regions if r not in excluded_regions]
        # exclude not opted in regions
        if not_opted_in_regions:
            regions = [r for r in regions if r not in not_opted_in_regions]

        return regions

    def _instantiate_facades(self):
        self.ec2 = EC2Facade(self.session, self.owner_id)
        self.acm = AcmFacade(self.session)
        self.awslambda = LambdaFacade(self.session)
        self.cloudformation = CloudFormation(self.session)
        self.cloudtrail = CloudTrailFacade(self.session)
        self.cloudwatch = CloudWatch(self.session)
        self.config = ConfigFacade(self.session)
        self.directconnect = DirectConnectFacade(self.session)
        self.dynamodb = DynamoDBFacade(self.session)
        self.efs = EFSFacade(self.session)
        self.elasticache = ElastiCacheFacade(self.session)
        self.emr = EMRFacade(self.session)
        self.route53 = Route53Facade(self.session)
        self.elb = ELBFacade(self.session)
        self.elbv2 = ELBv2Facade(self.session)
        self.iam = IAMFacade(self.session)
        self.kms = KMSFacade(self.session)
        self.rds = RDSFacade(self.session)
        self.redshift = RedshiftFacade(self.session)
        self.s3 = S3Facade(self.session)
        self.ses = SESFacade(self.session)
        self.sns = SNSFacade(self.session)
        self.sqs = SQSFacade(self.session)
        self.secretsmanager = SecretsManagerFacade(self.session)

        # Instantiate facades for proprietary services
        try:
            self.cognito = CognitoFacade(self.session)
        except NameError:
            pass
        try:
            self.docdb = DocDBFacade(self.session)
        except NameError:
            pass
        try:
            self.ecs = ECSFacade(self.session)
        except NameError:
            pass
        try:
            self.ecr = ECRFacade(self.session)
        except NameError:
            pass
        try:
            self.eks = EKSFacade(self.session)
        except NameError:
            pass
        try:
            self.guardduty = GuardDutyFacade(self.session)
        except NameError:
            pass