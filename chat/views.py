from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Message
from accounts.models import User
from django.db.models import Max

@login_required
def inbox(request):
    # Show conversations (last message per user)
    sent = Message.objects.filter(sender=request.user).values('receiver').annotate(last=Max('timestamp'))
    received = Message.objects.filter(receiver=request.user).values('sender').annotate(last=Max('timestamp'))

    # Combine and get unique conversation partners
    conversations = {}
    for msg in sent:
        user_id = msg['receiver']
        conversations[user_id] = msg['last']
    for msg in received:
        user_id = msg['sender']
        if user_id not in conversations or msg['last'] > conversations[user_id]:
            conversations[user_id] = msg['last']

    # Get user objects and last message
    conv_list = []
    for user_id, last_time in conversations.items():
        other_user = get_object_or_404(User, id=user_id)
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
        ).order_by('-timestamp').first()

        conv_list.append({
            'other_user': other_user,
            'last_message': last_msg,
            'unread_count': Message.objects.filter(receiver=request.user, sender=other_user, is_read=False).count()
        })

    # Sort by most recent
    conv_list.sort(key=lambda x: x['last_message'].timestamp if x['last_message'] else timezone.now(), reverse=True)

    return render(request, 'chat/inbox.html', {'conversations': conv_list})

@login_required
def chat_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Security: only allow teacher ↔ learner or admin
    # Security: allow teacher ↔ learner AND learner ↔ learner
    if not (
      (request.user.is_teacher and other_user.is_learner) or
      (request.user.is_learner and other_user.is_teacher) or
      (request.user.is_learner and other_user.is_learner) or   # ← added this line
      request.user.is_admin):
      messages.error(request, "You can only chat with teachers or other learners.")
      return redirect('chat:inbox')
    

    # Mark as read
    Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).update(is_read=True)

    messages_list = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('chat:detail', user_id=user_id)

    return render(request, 'chat/detail.html', {
        'other_user': other_user,
        'messages': messages_list
    })
    
@login_required
def my_learners(request):
    if request.user.role != 'teacher':
        messages.error(request, "Only teachers can view this page.")
        return redirect('chat:inbox')

    # For now, show all learners (later filter by class/grade)
    learners = User.objects.filter(role='learner').order_by('username')

    return render(request, 'chat/my_learners.html', {'learners': learners})
    
    
@login_required
def my_classmates(request):
    if request.user.role != 'learner':
        messages.error(request, "Only learners can access this page.")
        return redirect('chat:inbox')

    # Show all other learners (later you can filter by same grade/class)
    classmates = User.objects.filter(
        role='learner'
    ).exclude(id=request.user.id).order_by('username')

    return render(request, 'chat/my_classmates.html', {
        'classmates': classmates
    })