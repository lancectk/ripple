"""temporal_graph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from api.views import GraphConstructionView, UserWeightView, WeightView, AdjacencyView

urlpatterns = [
    # GraphConstructionView POST
    url(r'^graph/(?P<temporal_graph_id>\w{1,50})/(?P<weight_id>\w{1,50})$', GraphConstructionView.as_view()),

    # only GET on WeightView is implemented
    url(
        r'^weight/(?P<temporal_graph_id>\w{1,50})/(?P<weight_id>\w{1,50})/'
        r'(?P<source_vertex_id>\w{1,50})/(?P<target_vertex_id>\w{1,50})$',
        WeightView.as_view()
    ),

    # AdjacencyView GET
    url(
        r'^adjacent/(?P<temporal_graph_id>\w{1,50})/(?P<weight_id>\w{1,50})/(?P<source_vertex_id>\w{1,50})$',
        AdjacencyView.as_view()
    ),

    # UserWeightView GET
    url(
        r'^user-weight/(?P<temporal_graph_id>\w{1,50})/(?P<weight_id>\w{1,50})/'
        r'(?P<source_vertex_id>\w{1,50})/(?P<target_vertex_id>\w{1,50})$',
        UserWeightView.as_view()
    ),

    # UserWeightView POST
    url(
        r'^user-weight/(?P<temporal_graph_id>\w{1,50})/(?P<weight_id>\w{1,50})',
        UserWeightView.as_view()
    ),
]
