from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from resources.models import Resource
from admissions.models import AdmissionApplication
from announcements.models import Announcement
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from accounts.models import User
from chat.models import Message
from django.db.models import Q
# For role checks – add these class-based if you prefer over functions


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'admin'

class AdminDashboardView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # User statistics
        context['total_users'] = User.objects.count()
        context['total_students'] = User.objects.filter(role='learner').count()
        context['total_teachers'] = User.objects.filter(role='teacher').count()
        context['total_parents'] = User.objects.filter(role='parent').count()

        # Admissions statistics
        context['pending_admissions'] = AdmissionApplication.objects.filter(status='pending').count()
        context['approved_admissions'] = AdmissionApplication.objects.filter(status='approved').count()
        context['rejected_admissions'] = AdmissionApplication.objects.filter(status='rejected').count()
        context['total_applications'] = AdmissionApplication.objects.count()

        # Recent activity
        context['recent_announcements'] = Announcement.objects.select_related('author').order_by('-created_at')[:5]
        context['recent_resources'] = Resource.objects.select_related('uploaded_by').order_by('-created_at')[:5]
        context['recent_messages'] = Message.objects.select_related('sender', 'receiver').order_by('-timestamp')[:5]

        # Quick counts for charts / highlights
        context['unread_messages_count'] = Message.objects.filter(is_read=False).count()

        return context
        
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_admin

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher

class ParentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_parent

class LearnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_learner

class LearnerDashboardView(LearnerRequiredMixin, TemplateView):
    template_name = 'dashboard/learner.html'

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
    
      user_grade = self.request.user.grade
    
      context['latest_resources'] = Resource.objects.filter(
        Q(grade=user_grade) | Q(grade__isnull=True) ).order_by('-created_at')[:5]
    
      context['latest_announcements'] = Announcement.objects.filter(
        Q(grade=user_grade) | Q(grade__isnull=True),
        is_active=True).order_by('-created_at')[:5]
      return context

class TeacherDashboardView(TeacherRequiredMixin, TemplateView):
    template_name = 'dashboard/teacher.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pull dummy/future data
        context['recent_resources'] = []  # Later: Resource.objects.filter(class=self.request.user.classroom)[:5]
        context['unread_messages'] = 2    # Later: count from chat app
        context['announcements'] = []     # Later: from announcements app
        return context
        

class ParentDashboardView(ParentRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/parent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user'] = self.request.user
        # In parent_dashboard or ParentDashboardView
        context['latest_resources'] = Resource.objects.filter(grade__isnull=True  ).order_by('-created_at')[:5]

        context['latest_announcements'] = Announcement.objects.filter(is_active=True,grade__isnull=True  ).order_by('-created_at')[:5]

        context['latest_resources'] = Resource.objects.filter(grade__isnull=True).order_by('-created_at')[:5]
        
        
        
        context['applications'] = AdmissionApplication.objects.filter(
            parent=self.request.user
        ).order_by('-submitted_at')
        
        return context
# Do similar for other roles:
# class TeacherDashboardView(TeacherRequiredMixin, TemplateView): ...
# etc.

# Update urls.py to use these classes
# In dashboard/urls.py:
 # ← import

# For function-based view (example for learner_dashboard)
