from wpaudit.providers.gcp.resources.gke.clusters import Clusters
from wpaudit.providers.gcp.resources.zones import Zones


class GKEZones(Zones):
    _children = [
        (Clusters, 'clusters'),
    ]
