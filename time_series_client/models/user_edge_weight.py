from time_series_client.models.timestamp_model import TimestampModel
from time_series_client.models.graph_version import GraphVersion

from django.db import models

class UserEdgeWeight(TimestampModel):
    """
    Time series that tracks edge weight for a particular user

    """
    user_id   = models.IntegerField(null=False)

    edge_id   = models.CharField(max_length=64, null=False)

    weight_id = models.CharField(max_length=64, null=False)

    weight    = models.FloatField(null=False)

    graph_version = models.ForeignKey(GraphVersion, null=False)

    class Meta:
        unique_together = ('user_id', 'edge_id', 'weight_id')
