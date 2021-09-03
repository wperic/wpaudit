from wpaudit.providers.gcp.resources.gce.subnetworks import Subnetworks
from wpaudit.providers.gcp.resources.regions import Regions


class GCERegions(Regions):
    _children = [
        (Subnetworks, 'subnetworks')
    ]
