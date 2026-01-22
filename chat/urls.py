from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<int:user_id>/', views.chat_detail, name='detail'),
    path('my-learners/', views.my_learners, name='my_learners'),
    
    # ... your existing paths ...
    path('my-classmates/', views.my_classmates, name='my_classmates'),

]