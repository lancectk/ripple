import logging
import os
from graph_client.graph_client import GraphClient

from neo4j.v1 import GraphDatabase

logger = logging.getLogger(__name__)

class NeoGraphClient(GraphClient):
    """
    NeoGraph client is a Neo4j implemention of GraphClient

    """

    def __init__(self,
                 graph_uuid,
                 neojs_url = os.environ['GRAPHENEDB_BOLT_URL'],
                 neojs_username = os.environ['GRAPHENEDB_BOLT_USER'],
                 neojs_password = os.environ['GRAPHENEDB_BOLT_PASSWORD']):

        self.graph_uuid = graph_uuid
        self.driver = GraphDatabase.driver(neojs_url, auth=(neojs_username, neojs_password))


    def run_query(self, query):
        """
        Safely run a query. Ensure session is property initialized and closed.
        Equivalent of a managed resource

        :param query: query to run
        :return: BoltStatementResult
        """
        try:
            session = self.driver.session()

            statement_result = session.run(query)

            session.close()

            return statement_result
        except Exception as error:
            logging.error(f'Failed to run Neo4j query {query}, error: {error}')
        finally:
            session.close()

        return None


    def get_vertex_property(self, vertex_id, prop_key):
        """
        Gets vertex property of the vertex identified by vertex_id

        :param vertex_id: uuid identifying the vertex
        :param prop_key: desired property key
        :return:  [String] property value or empty string if edge does not exist, property does not exist or error
        """

        cypher_query = f"""
          MATCH 
          (sv:Vertex)
          WHERE sv.vertex_id="{vertex_id}" AND sv.graph_uuid="{self.graph_uuid}"
          RETURN sv.{prop_key}
          """

        bolt_statement_res = self.run_query(cypher_query)

        if bolt_statement_res:
            query_results = [res[f'sv.{prop_key}'] for res in bolt_statement_res]

            if len(query_results) > 1:
                logger.error(f'Violation: more than one Vertex has the id: {vertex_id}')
            elif len(query_results) == 1:
                return query_results[0]

        return ""


    def set_vertex_property(self, vertex_id, prop_key, prop_value):
        """
        Sets vertex property of the vertex identified by vertex_id.
        Creates vertex if does not exist

        :param vertex_id: uuid identifying the vertex
        :param prop_key: desired property key
        :param prop_value: desired property value
        :return: [Bool] successful setting property or not
        """

        cypher_query = f"""
            MERGE (sv:Vertex {{vertex_id:"{vertex_id}",graph_uuid:"{self.graph_uuid}"}})
            ON CREATE SET sv.{prop_key}="{prop_value}"
            ON MATCH SET sv.{prop_key}="{prop_value}"
            """

        bolt_statement_res = self.run_query(cypher_query)

        return True if bolt_statement_res else False

    def get_edge_property(self, source_vertex_id, target_vertex_id, prop_key):
        """
        Gets edge property of the edge connecting source and target vertex

        :param source_vertex_id: uuid identifying the source vertex id
        :param target_vertex_id: uuid identifying the target vertex id
        :param prop_key: desired property key
        :return: [String] property value or empty string if edge does not exist, property does not exist or error
        """

        cypher_query = f"""
          MATCH 
          (sv:Vertex {{vertex_id:"{source_vertex_id}",graph_uuid:"{self.graph_uuid}"}})
          -[e:CONNECTED_TO]->
          (tv:Vertex {{vertex_id:"{target_vertex_id}",graph_uuid:"{self.graph_uuid}"}})
          RETURN e.{prop_key}
          """

        bolt_statement_res = self.run_query(cypher_query)

        if bolt_statement_res:
            query_results = [res[f'e.{prop_key}'] for res in bolt_statement_res]

            if len(query_results) > 1:
                logger.error(f'Violation: more than one Edge between vertices {source_vertex_id} and {target_vertex_id}')
            elif len(query_results) == 1:
                return query_results[0]

        return ""

    def set_edge_property(self, source_vertex_id, target_vertex_id, prop_key, prop_value):
        print("SETTING EDGE PROPERTY")
        """
        Sets edge property of the edge connecting source and target vertex.
        Creates source/target vertex and edge if does not exist

        :param source_vertex_id:
        :param target_vertex_id:
        :param property_key:
        :param property_value:
        :return: edge_id
        """

        cypher_query = f"""
          MERGE (sv:Vertex {{vertex_id:"{source_vertex_id}",graph_uuid:"{self.graph_uuid}"}})
          MERGE (tv:Vertex {{vertex_id:"{target_vertex_id}",graph_uuid:"{self.graph_uuid}"}})
          MERGE (sv)-[e:CONNECTED_TO]->(tv)
          ON CREATE SET e.{prop_key}="{prop_value}"
          ON MATCH SET e.{prop_key}="{prop_value}"
          """

        bolt_statement_res = self.run_query(cypher_query)

        return True if bolt_statement_res else False