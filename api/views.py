from restless.views import Endpoint
import json
from django.http import HttpResponseBadRequest, HttpResponseServerError

from temporal_graph_engine.temporal_graph_engine import TemporalGraphEngine

import logging

logger = logging.getLogger(__name__)

class GraphConstructionView(Endpoint):
    def post(self, request, temporal_graph_id, weight_id):

        try:
            decoded_body_unicode = request.body.decode('utf-8')
            body = json.loads(decoded_body_unicode)

            version_id         = int(body['version_id'])

            # payload contains graph elements to update
            graph_elements    = body['payload']

            commit            = body['commit']

        except:
            logger.error(f'Error parsing body of the message: {body}.'
                         f'Ensure fields and format of body is correct. See docs.')

            return HttpResponseBadRequest(f'Error parsing body of the message: {body}. '
                                          'Ensure fields and format of body is correct. See docs.')

        try:
            tge = TemporalGraphEngine()

            success = tge.construct_graph(temporal_graph_id, weight_id, version_id, graph_elements, commit)
        except:
            logger.error(f'Payload error. Ensure payload format is correct: {graph_elements}')
            return HttpResponseBadRequest(f'Payload error. Ensure payload format is correct: {graph_elements}')


        return { 'success': success, 'temporal_graph_id': weight_id, 'version_id': version_id }


class WeightView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id, target_vertex_id):

        try:
            timestamp  = request.GET.get('timestamp', None)
            version_id = request.GET.get('version_id', None)

            if version_id:
                version_id = int(version_id)

            if timestamp:
                timestamp = int(timestamp)
        except:
            logger.error(f'Error parsing URL params: {request.GET}. timestamp and version must be Int. See docs.')

            return HttpResponseBadRequest(f'Error parsing URL params: {request.GET}. '
                                          f'timestamp and version must be Int. See docs.')

        try:
            tge = TemporalGraphEngine()

            weight = tge.get_edge_weight(temporal_graph_id, weight_id,
                                         source_vertex_id, target_vertex_id,
                                         version_id, timestamp)
        except:
            logger.error(f'Application error while getting edge weight for request {request}.')

            return HttpResponseServerError(f'Application error while getting edge weight for request {request}.')

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id,
                'target_vertex_id': target_vertex_id, 'timestamp': timestamp, 'version_id': version_id, 'weight':weight }


class UserWeightView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id, target_vertex_id):

        timestamp  = request.GET.get('timestamp', '')
        version_id = request.GET.get('version_id', '')
        user_id    = request.GET.get('user_id', '')


        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id,
                'target_vertex_id': target_vertex_id, 'timestamp': timestamp, 'version_id': version_id, 'user_id': user_id}

    def post(self, request, temporal_graph_id, weight_id):
        decoded_body_unicode = request.body.decode('utf-8')
        body = json.loads(decoded_body_unicode)

        version_id = body['version_id']

        # payload contains graph elements to update
        graph_elements    = body['payload']

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'version_id': version_id,
                'payload': graph_elements }



class AdjacencyView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id):

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id }

