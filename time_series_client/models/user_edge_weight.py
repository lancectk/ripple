from time_series_client.models.timestamp_model import TimestampModel
from time_series_client.models.graph_version import GraphVersion

from time_series_client.models.managers.core_manager import CoreManager

from django.db import models

from datetime import datetime

class UserEdgeWeight(TimestampModel):
    objects = CoreManager()

    """
    Time series that tracks edge weight for a particular user

    """
    user_id   = models.IntegerField(null=False)

    # an edge is uniquely identified by its source and target vertices
    source_vertex_id   = models.CharField(max_length=64, null=False)
    target_vertex_id   = models.CharField(max_length=64, null=False)

    weight_id = models.CharField(max_length=64, null=False)

    weight    = models.FloatField(null=True)

    graph_version = models.ForeignKey(GraphVersion, null=False)

    def commit_version(self):
        self.committed_at = datetime.now()

        self.save()


    class Meta:
        unique_together = ('graph_version', 'user_id', 'source_vertex_id', 'target_vertex_id', 'weight_id')
