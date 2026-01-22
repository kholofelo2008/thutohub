from django.urls import path
from . import views   # we'll create views next

app_name = 'dashboard'   # ← This is what registers the 'dashboard' namespace!

urlpatterns = [
    # Temporary placeholder views – we'll fill them properly soon
    path('school-admin/', views.AdminDashboardView.as_view(),
    name='admin_dashboard'),
    path('teacher/', views.TeacherDashboardView.as_view(), name='teacher'),
    path('parent/', views.ParentDashboardView.as_view(), name='parent'),
    path('learner/', views.LearnerDashboardView.as_view(), name='learner'),
]