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
            err_msg = f'Error parsing body of the message: {body}. ' \
                      f'Ensure fields and format of body is correct. See docs.'

            logger.error(err_msg)
            return HttpResponseBadRequest(err_msg)

        try:
            tge = TemporalGraphEngine()

            success = tge.construct_graph(temporal_graph_id, weight_id, version_id, graph_elements, commit)
        except:
            err_msg = f'Payload error. Ensure payload format is correct: {graph_elements}'

            logger.error(err_msg)
            return HttpResponseBadRequest(err_msg)


        return { 'success': success, 'temporal_graph_id': weight_id, 'version_id': version_id }


class WeightView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id, target_vertex_id):

        try:
            timestamp  = request.GET.get('timestamp', None)
            timestamp = int(timestamp) if timestamp else None

            version_id = request.GET.get('version_id', None)
            version_id = int(version_id) if version_id else None
        except:
            err_msg = f'Error parsing URL params: {request.GET}. timestamp and version must be Int. See docs.'

            logger.error(err_msg)
            return HttpResponseBadRequest(err_msg)

        try:
            tge = TemporalGraphEngine()

            weight = tge.get_edge_weight(temporal_graph_id, weight_id,
                                         source_vertex_id, target_vertex_id,
                                         version_id, timestamp)

            weight = float(weight) if weight else None
        except:
            err_msg = f'Application error while getting edge weight for request {request}.'

            logger.error(err_msg)
            return HttpResponseServerError(err_msg)

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id,
                'target_vertex_id': target_vertex_id, 'timestamp': timestamp, 'version_id': version_id, 'weight': weight }


class UserWeightView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id, target_vertex_id):
        try:
            timestamp  = request.GET.get('timestamp', None)
            timestamp = int(timestamp) if timestamp else None

            version_id = request.GET.get('version_id', None)
            version_id = int(version_id) if version_id else None

            user_id    = request.GET.get('user_id', None)
            user_id    = int(user_id) if user_id else None
        except:
            logger.error(f'Error parsing URL params: {request.GET}.'
                         f'timestamp, version_id and user_id must be Int. See docs.')

            return HttpResponseBadRequest(f'Error parsing URL params: {request.GET}.'
                         f'timestamp, version_id and user_id must be Int. See docs.')

        try:
            tge = TemporalGraphEngine()

            weight = tge.get_user_edge_weight(temporal_graph_id, weight_id,
                                              source_vertex_id, target_vertex_id,
                                              user_id, version_id, timestamp)
            weight = float(weight) if weight else None

        except:
            err_msg = f'Application error while getting user edge weight for request {request}.'

            logger.error(err_msg)
            return HttpResponseServerError(err_msg)

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id,
                 'source_vertex_id': source_vertex_id, 'target_vertex_id': target_vertex_id,
                 'timestamp': timestamp, 'version_id': version_id,
                 'user_id': user_id, 'weight': weight}


    def post(self, request, temporal_graph_id, weight_id):
        try:
            decoded_body_unicode = request.body.decode('utf-8')
            body = json.loads(decoded_body_unicode)

            # payload contains graph elements to update
            graph_elements    = body['payload']
        except:
            err_msg = f'Error parsing body of the message: {body}. ' \
                      f'Ensure fields and format of body is correct. See docs.'

            logger.error(err_msg)
            return HttpResponseBadRequest(err_msg)

        try:
            tge = TemporalGraphEngine()
            success = tge.set_user_edge_weight(temporal_graph_id, weight_id, graph_elements)

            if not success:
                err_msg = f'Failed to write user-edge weight.' \
                          f'Ensure committed temporal graph with id: {temporal_graph_id} exists.' \
                          f'Ensure base edge for each user-edge weight exists'

                logger.error(err_msg)
                return HttpResponseBadRequest(err_msg)
        except:
            err_msg = f'Payload error. Ensure payload format is correct: {graph_elements}'
            logger.error(err_msg)
            return HttpResponseBadRequest(err_msg)

        return { 'temporal_graph_id': temporal_graph_id, 'success': success}



class AdjacencyView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id):
        # TODO: unimplemented

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id }

