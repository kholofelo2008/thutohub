from django.urls import path
from .views import ResourceListView, ResourceUploadView

app_name = 'resources'

urlpatterns = [
    path('', ResourceListView.as_view(), name='list'),
    path('upload/', ResourceUploadView.as_view(), name='upload'),
]