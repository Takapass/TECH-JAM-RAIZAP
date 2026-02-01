from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Activity


def activity_list(request):
    if request.method == "POST":
        for activity in Activity.objects.all():
            if str(activity.id) in request.POST:
                activity.is_done = True
                activity.save()

        messages.success(request, '保存しました！')

        Activity.objects.update(is_done=False)

        return redirect('activity_list')

    activities = Activity.objects.all()
    return render(request, 'activities/activity_list.html', {
        'activities': activities
    })


def home(request):
    activities = Activity.objects.all()
    return render(request, 'activities/home.html', {
        'activities': activities
    })


def group(request):
    return render(request, 'activities/group.html')


def idea(request):
    return render(request, 'activities/idea.html')