from wpaudit.providers.gcp.resources.gce.instances import Instances
from wpaudit.providers.gcp.resources.zones import Zones


class GCEZones(Zones):
    _children = [
        (Instances, 'instances'),
    ]
