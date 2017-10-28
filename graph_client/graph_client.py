from neo4j.v1 import GraphDatabase

class GraphClient():
    """
    The following are required of GraphClient implementations:
      1. All references to vertices and edges must be associated with a graph_uuid. This is set upon initialization
         of GraphClient, and all succeeding calls will be associated with the graph_uuid
      2. Each vertex and edge to have a bag of properties that can be set and get
      3. Vertices and edges to have a unique *_id (although edges are typically referenced by its vertex pair)
      4. Transactional operations

    """
    class Meta:
        abstract = True

    def __init__(self, graph_uuid):
        """
        Associate this GraphClient with a particular graph_uuid.
        Get and Set elements for the given graph_uuid

        :param graph_uuid:
        """
        self.graph_uuid = graph_uuid

    def get_vertex_property(self, vertex_id, prop_key, prop_value):
        """
        Gets vertex property of the vertex identified by vertex_id

        :param vertex_id: uuid identifying the vertex
        :param prop_key: desired property key
        :return:  [String] property value or empty string if edge does not exist, property does not exist or error
        """

        raise NotImplementedError('GraphClient#get_vertex_property must be implemented')

    def set_vertex_property(self, vertex_id, prop_key, prop_value):
        """
        Sets vertex property of the vertex identified by vertex_id.
        Creates vertex if does not exist

        :param vertex_id: uuid identifying the vertex
        :param prop_key: desired property key
        :param prop_value: desired property value
        :return: [Bool] successful setting property or not
        """

        raise NotImplementedError('GraphClient#set_vertex_property must be implemented')

    def get_edge_property(self, source_vertex_id, target_vertex_id):
        """
        Gets edge property of the edge connecting source and target vertex

        :param source_vertex_id: uuid identifying the source vertex id
        :param target_vertex_id: uuid identifying the target vertex id
        :param prop_key: desired property key
        :return: [String] property value or empty string if edge does not exist, property does not exist or error
        """

        raise NotImplementedError('GraphClient#get_edge_property must be implemented')

    def set_edge_property(self, source_vertex_id, target_vertex_id, prop_key, prop_value):
        """
        Sets edge property of the edge connecting source and target vertex.
        Creates source/target vertex and edge if does not exist

        :param source_vertex_id:
        :param target_vertex_id:
        :param property_key:
        :param property_value:
        :return: edge_id
        """

        raise NotImplementedError('GraphClient#set_edge_property must be implemented')







