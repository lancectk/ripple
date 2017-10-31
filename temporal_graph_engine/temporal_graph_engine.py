from graph_client.neo_graph_client import NeoGraphClient
from time_series_client.models.graph_version import GraphVersion
from time_series_client.models.user_edge_weight import UserEdgeWeight

import logging

logger = logging.getLogger(__name__)

class TemporalGraphEngine():
    def get_graph_client(self, graph_uuid):
        """
        GraphClient used to travese graph

        :param graph_uuid:
        :return:
        """
        return NeoGraphClient(graph_uuid)

    @classmethod
    def get_graph_version_model(cls):
        """
        ORM to get and set Graph Versions

        :return:
        """
        return GraphVersion

    @classmethod
    def get_user_edge_weight_model(cls):
        """
        ORM to get and set User Edge Weights

        :return:
        """
        return UserEdgeWeight

    def get_graph_version(self, temporal_graph_id, version_id = None, timestamp = None):
        """
        Retrieves the committed version of a temporal graph based on (in order of priority):
         1. version_id - retrieve specific verison
         2. timestamp  - retrieves the committed version at this point in time
         3. latest version of temporal graph
        :param temporal_graph_id:
        :param version_id:
        :param timestamp:
        :return:
        """
        if version_id:
            # retrieve specific version
             graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                 temporal_graph_id=temporal_graph_id,
                 version_id=int(version_id),
                 committed=True
            )
        elif timestamp:
            # retrieve latest version committed before this timestamp (latest at that point)
            graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                temporal_graph_id=temporal_graph_id,
                committed_at__lte=timestamp,
                committed=True
            )
        else:
            # get latest graph verison
            graph_version = TemporalGraphEngine.get_graph_version_model().objects.get_latest_or_none('committed_at',
                temporal_graph_id=temporal_graph_id,
                committed=True
            )

        return graph_version

    def get_graph_version_edge_weight(self, graph_version, source_vertex_id, target_vertex_id, weight_id):
        """
        Retrieves edge weight of a particular graph_version

        :param graph_version: [GraphVersion]
        :param source_vertex_id: [String]
        :param target_vertex_id: [String]
        :param weight_id: [String]
        :return: [Float] weight or None if it does not exist
        """
        graph_client = self.get_graph_client(graph_version.graph_uuid)

        weight = graph_client.get_edge_property(source_vertex_id, target_vertex_id, weight_id)

        if not weight:
            return None
        else:
            return weight

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
            # graph_version has been previously committed
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

        graph_version = self.get_graph_version(temporal_graph_id, version_id, timestamp)

        if graph_version:
            return self.get_graph_version_edge_weight(graph_version, source_vertex_id, target_vertex_id, weight_id)
        else:
            return None

    def get_user_edge_weight(self,
                        temporal_graph_id,
                        weight_id,
                        source_vertex_id,
                        target_vertex_id,
                        user_id,
                        version_id = None,
                        timestamp  = None
                        ):
        """
        Retrieve edge weight for a a specific user, specific version

        :param temporal_graph_id:[String]
        :param weight_id:[String]
        :param source_vertex_id:[String]
        :param target_vertex_id:[String]
        :param user_id:[Int]
        :param version_id:[int] If version_id is passed in, timestamp is ignored and the user edge of
                 the graph at this specific version is returned
        :param timestamp:[Int] Unix epoch. user edge of the graph at this point in time
        :return: [Float] user-edge weight if exists, else edge weight
                           else None (if version of graph doesn't exist or edge does not exist)
        """

        graph_version = self.get_graph_version(temporal_graph_id, version_id, timestamp)

        if graph_version:
            user_edge_weight = TemporalGraphEngine.get_user_edge_weight_model().objects.get_latest_or_none(
                'committed_at',
                user_id=user_id,
                source_vertex_id=source_vertex_id,
                target_vertex_id=target_vertex_id,
                weight_id=weight_id,
                graph_version=graph_version
            )

            if user_edge_weight:
                return user_edge_weight.weight
            else:
                return self.get_graph_version_edge_weight(graph_version, source_vertex_id, target_vertex_id, weight_id)

    def set_user_edge_weight(self,
                        temporal_graph_id,
                        weight_id,
                        vertex_edge_pairs
                        ):
        """
        Set user edge weight for latest graph version of temporal_graph_id

        :param temporal_graph_id: [String]
        :param weight_id: [String]
        :param vertex_edge_pairs: List[{
              "user_id":123,
              "source_vertex_id": "vert1",
              "target_vertex_id": "vert2",
              "weight": 0.72
          }, {..}]
        :return: True if successfully set all user-edges
        """

        graph_version = self.get_graph_version(temporal_graph_id, None, None)

        if graph_version:
            graph_client = self.get_graph_client(graph_version.graph_uuid)

            successful_writes = []

            for user_vertex_edge_pair in vertex_edge_pairs:
                user_id          = user_vertex_edge_pair['user_id']
                source_vertex_id = user_vertex_edge_pair['source_vertex_id']
                target_vertex_id = user_vertex_edge_pair['target_vertex_id']
                weight           = user_vertex_edge_pair['weight']

                base_weight = graph_client.get_edge_property(source_vertex_id, target_vertex_id, weight_id)

                if base_weight:
                    user_edge_weight, created = TemporalGraphEngine.get_user_edge_weight_model().objects.get_or_create(
                        graph_version=graph_version,
                        user_id=user_id,
                        source_vertex_id=source_vertex_id,
                        target_vertex_id=target_vertex_id,
                        weight_id=weight_id
                    )
                    user_edge_weight.weight = weight
                    user_edge_weight.save()

                    user_edge_weight.commit_version()

                    successful_writes.append(True)
            # TODO(lcotingkeh): accumulate errors and return to user

            return len(successful_writes) == len(vertex_edge_pairs)
        else:
            return False