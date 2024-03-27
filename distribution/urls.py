from django.urls import path
from django.views.decorators.cache import cache_page

from distribution.apps import DistributionConfig
from distribution.views import (ClientListView, ClientDetailView, ClientCreateView, ClientDeleteView,
                                ClientUpdateView, HomeTemplateView, contact, CircularListView, CircularDetailView,
                                CircularCreateView, CircularDeleteView, CircularUpdateView, MessageCreateView,
                                MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView)

app_name = DistributionConfig.name


urlpatterns = [
    path('', cache_page(60)(HomeTemplateView.as_view()), name='home'),
    path("client/add/", ClientCreateView.as_view(), name='client_create'),
    path("clients", ClientListView.as_view(), name='client_list'),
    path("client/<int:pk>/", ClientDetailView.as_view(), name='client_detail'),
    path("client/<int:pk>/update", ClientUpdateView.as_view(), name='client_update'),
    path("client/<int:pk>/delete", ClientDeleteView.as_view(), name='client_delete'),
    path("circular/add/", CircularCreateView.as_view(), name='circular_create'),
    path("circulars", CircularListView.as_view(), name='circular_list'),
    path("circular/<int:pk>/", CircularDetailView.as_view(), name='circular_detail'),
    path("circular/<int:pk>/update", CircularUpdateView.as_view(), name='circular_update'),
    path("circular/<int:pk>/delete", CircularDeleteView.as_view(), name='circular_delete'),
    path("message/add/", MessageCreateView.as_view(), name='message_create'),
    path("messages", MessageListView.as_view(), name='message_list'),
    path("message/<int:pk>/", MessageDetailView.as_view(), name='message_detail'),
    path("message/<int:pk>/update", MessageUpdateView.as_view(), name='message_update'),
    path("message/<int:pk>/delete", MessageDeleteView.as_view(), name='message_delete'),
    path('contact/', contact, name='contact'),
]
