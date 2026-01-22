from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Resource
from .forms import ResourceUploadForm

class ResourceListView(LoginRequiredMixin, ListView):
    model = Resource
    template_name = 'resources/list.html'
    context_object_name = 'resources'

    def get_queryset(self):
        qs = super().get_queryset()
        grade = self.request.user.grade
        
        if grade:
            qs = qs.filter(
                Q(grade=grade) | Q(grade__isnull=True)
            )
        
        return qs


class ResourceUploadView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceUploadForm
    template_name = 'resources/upload.html'
    success_url = '/resources/'  # change to reverse_lazy('resources:list') later if needed

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)