from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import AdmissionApplication
from .forms import AdmissionApplicationForm

@login_required
def admission_apply(request):
    if request.user.role != 'parent':
        messages.error(request, "Only parents can submit admission applications.")
        return redirect('dashboard:learner')

    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.parent = request.user
            application.save()
            messages.success(request, "Your child's application has been submitted successfully. We will review it shortly.")
            return redirect('dashboard:parent')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AdmissionApplicationForm()

    return render(request, 'admissions/apply.html', {'form': form})

@login_required
def admission_list(request):
    if request.user.role != 'admin':
        messages.error(request, "Only administrators can access this page.")
        return redirect('dashboard:admin')

    applications = AdmissionApplication.objects.all().order_by('-submitted_at')
    return render(request, 'admissions/list.html', {'applications': applications})

@login_required
def admission_review(request, pk):
    if request.user.role != 'admin':
        return redirect('dashboard:learner')

    application = get_object_or_404(AdmissionApplication, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('admin_notes', '')
        if new_status in ['approved', 'rejected', 'waitlist']:
            application.status = new_status
            application.admin_notes = notes
            application.reviewed_by = request.user
            application.reviewed_at = timezone.now()
            application.save()
            messages.success(request, f"Application has been {new_status}.")
            return redirect('admissions:list')

    return render(request, 'admissions/review.html', {'application':
    application})