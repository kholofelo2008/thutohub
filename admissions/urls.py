from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('apply/', views.admission_apply, name='apply'),
    path('', views.admission_list, name='list'),
    path('<int:pk>/review/', views.admission_review, name='review'),
]