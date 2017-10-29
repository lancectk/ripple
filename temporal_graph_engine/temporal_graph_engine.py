from graph_client.neo_graph_client import NeoGraphClient
from time_series_client.models.graph_version import GraphVersion
from time_series_client.models.user_edge_weight import UserEdgeWeight

import logging

logger = logging.getLogger(__name__)

class TemporalGraphEngine():
    def get_graph_client(self, graph_uuid):
        return NeoGraphClient(graph_uuid)

    @classmethod
    def get_graph_version_model(cls):
        return GraphVersion

    def construct_graph(self,
                        temporal_graph_id,
                        weight_id,
                        version_id,
                        vertex_edge_pairs,
                        commit = False):
        """
        Construct/add to an uncommitted temporal graph.
        Once a graph version is committed, it is immutable and cannot be modified


        :param temporal_graph_id: [String]
        :param weight_id: [String]
        :param version_id: [Int]
        :param vertex_edge_pairs: List[{
              "source_vertex_id": "vert1",
              "target_vertex_id": "vert2"
              "weight":0.65
          },{..}]
        :param commit: [Bool]
        :return: [Bool]. True if successfully constructed
                       False if data format error or trying to append to an immutable graph
        """

        graph_version, created = TemporalGraphEngine.get_graph_version_model().objects.get_or_create(
            temporal_graph_id = temporal_graph_id,
            version_id        = int(version_id)
        )

        if graph_version.committed:
            logger.error(f'TemporalGraph with id:{temporal_graph_id} and version: {version_id} cannot be'
                         f' modified since it has previously been COMMITTED')

            return False
        else:
            graph_client = self.get_graph_client(graph_version.graph_uuid)

            for vertex_edge in vertex_edge_pairs:
                graph_client.set_edge_property(vertex_edge['source_vertex_id'],
                                               vertex_edge['target_vertex_id'],
                                               weight_id,
                                               float(vertex_edge['weight'])
                                               )

        if commit:
            graph_version.commit_version()

        return True

    def get_edge_weight(self,
                        temporal_graph_id,
                        weight_id,
                        source_vertex_id,
                        target_vertex_id,
                        version_id = None,
                        timestamp  = None
                        ):
        """
        Retrieve weight of an edge of a (committed) temporal graph version at a given point in time

        :param temporal_graph_id: [String]
        :param weight_id: [String]
        :param source_vertex_id: [String]
        :param target_vertex_id: [String]
        :param version_id: [Int] If version_id is passed in, timestamp is ignored and the edge of
                 the graph at this specific version is returned
        :param timestamp: [Int] Unix epoch. edge of the graph at this point in time
        :return: [Float] weight if edge with weight_id exists
                           else None (if version of graph doesn't exist or edge does not exist)
        """
        if version_id:
            # get latest verison, or verison or timestmap
             graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                 temporal_graph_id=temporal_graph_id,
                 version_id=int(version_id),
                 committed=True
            )
        elif timestamp:
            graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                temporal_graph_id=temporal_graph_id,
                committed_at__lte=timestamp,
                committed=True
            )
        else:
            graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                temporal_graph_id=temporal_graph_id,
                committed=True
            )

        if graph_version:
            graph_client = self.get_graph_client(graph_version.graph_uuid)

            weight = graph_client.get_edge_property(source_vertex_id, target_vertex_id, weight_id)

            if not weight:
                return None
            else:
                return weight
        else:
            return None

