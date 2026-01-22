from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User   # ← this line fixes it


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'profile_picture']
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('dashboard:learner')  # or dynamic per role

    def get_object(self):
        return self.request.user

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        messages.success(self.request, "Account created! Please log in.")
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        # Redirect based on role after login
        user = self.request.user
        if user.is_admin:
            return reverse_lazy('dashboard:admin_dashboard')  # We'll create these later
        elif user.is_teacher:
            return reverse_lazy('dashboard:teacher')
        elif user.is_parent:
            return reverse_lazy('dashboard:parent')
        elif user.is_learner:
            return reverse_lazy('dashboard:learner')
        return reverse_lazy('core:home')  # Fallback

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
    # Add later: form to update profile pic, etc.