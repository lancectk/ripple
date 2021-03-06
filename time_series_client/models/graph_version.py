from datetime import datetime

from time_series_client.models.timestamp_model import TimestampModel

from django.db import models


class GraphVersion(TimestampModel):
    """
    GraphVersion model is a time series that tracks the versions of a temporal_graph_id

    It enforces uniquness in (temporal_graph_id, version_id) combinations

    """
    temporal_graph_id = models.CharField(max_length=64, null=False)
    version_id        = models.IntegerField(null=False)

    committed         = models.BooleanField(default=False)

    class Meta:
        unique_together = ('temporal_graph_id', 'version_id')

    @property
    def graph_uuid(self):
        """
        graph_uuid is a unique id for a particular temporal_graph_version

        :return:
        """
        return f'{self.temporal_graph_id}_v{self.version_id}'

    def commit_version(self):
        self.committed_at = datetime.now()
        self.committed    = True

        self.save()

    def __str__(self):
        return f'Graph temporal_graph_id [{self.temporal_graph_id}] | ' \
               f'version_id [{self.version_id}] |' \
               f'created at [{self.created_at}] |' \
               f'committed at [{self.committed_at}]'


