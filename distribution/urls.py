from django.urls import path
from distribution.apps import DistributionConfig
from distribution.views import (ClientListView, ClientDetailView, ClientCreateView, ClientDeleteView,
                                ClientUpdateView, HomeTemplateView)

app_name = DistributionConfig.name


urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path("clients", ClientListView.as_view(), name='client_list'),
    path("client/<int:pk>/", ClientDetailView.as_view(), name='client_detail'),
    path("client/add/", ClientCreateView.as_view(), name='client_create'),
    path("client/<int:pk>/update", ClientUpdateView.as_view(), name='client_update'),
    path("client/<int:pk>/delete", ClientDeleteView.as_view(), name='client_delete'),
]
