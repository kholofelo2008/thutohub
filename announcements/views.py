from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm

@login_required
def announcement_list(request):
    # Show only active ones
    announcements = Announcement.objects.filter(is_active=True).order_by('-created_at')

    # Optional: filter by role later
    if request.user.role == 'parent':
        announcements = announcements.filter(target_role__in=['all', 'parents'])
    elif request.user.role == 'learner':
        announcements = announcements.filter(target_role__in=['all', 'learners'])

    return render(request, 'announcements/list.html', {
        'announcements': announcements
    })

@login_required
def announcement_create(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can create announcements.")
        return redirect('dashboard:learner')

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, "Announcement posted successfully!")
            return redirect('announcements:list')
    else:
        form = AnnouncementForm()

    return render(request, 'announcements/create.html', {'form': form})

@login_required
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, is_active=True)
    return render(request, 'announcements/detail.html', {'announcement':
    announcement})