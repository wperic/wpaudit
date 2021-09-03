from wpaudit.providers.gcp.resources.projects import Projects
from wpaudit.providers.gcp.resources.iam.member_bindings import Bindings
from wpaudit.providers.gcp.resources.iam.users import Users
from wpaudit.providers.gcp.resources.iam.groups import Groups
from wpaudit.providers.gcp.resources.iam.service_accounts import ServiceAccounts


class IAM(Projects):
    _children = [
        (Bindings, 'bindings'),
        (Users, 'users'),
        (Groups, 'groups'),
        (ServiceAccounts, 'service_accounts')
    ]
