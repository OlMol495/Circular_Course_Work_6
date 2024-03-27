from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('list/', PostListView.as_view(), name='list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('post/<str:slug>/', PostDetailView.as_view(), name='detail'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='update'),
    path('post/<str:slug>/delete/', PostDeleteView.as_view(), name='delete'),
]