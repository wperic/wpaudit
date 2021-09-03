from wpaudit.providers.gcp.resources.kms.keyrings import KeyRings
from wpaudit.providers.gcp.resources.projects import Projects


class KMS(Projects):
    _children = [
        (KeyRings, 'keyrings')
    ]
