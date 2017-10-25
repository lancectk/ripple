from django.shortcuts import render

# Create your views here.



from restless.views import Endpoint
import json

class GraphConstructionView(Endpoint):
    def post(self, request, temporal_graph_id, weight_id):
        # print("DEBUGGING: ")
        # print(temporal_graph_id)
        # print(weight_id)

        decoded_body_unicode = request.body.decode('utf-8')
        body = json.loads(decoded_body_unicode)

        version_id        = body['version_id']

        # payload contains graph elements to update
        graph_elements    = body['payload']

        commit            = body['commit']

        return {'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'version_id': version_id,
                'payload': graph_elements, 'commit': commit}


class WeightView(Endpoint):
    def get(self, request, temporal_graph_id, weight_id, source_vertex_id, target_vertex_id):

        timestamp  = request.GET.get('timestamp', '')
        version_id = request.GET.get('version_id', '')

        return { 'temporal_graph_id': temporal_graph_id, 'weight_id': weight_id, 'source_vertex_id': source_vertex_id,
                'target_vertex_id': target_vertex_id, 'timestamp': timestamp, 'version_id': version_id }



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

