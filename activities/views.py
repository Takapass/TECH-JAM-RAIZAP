from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Activity
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# def login_view(request):
#     if request.method == "POST":
#         print("POST:", request.POST)
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)
#         print("USER:", user)

#         if user is not None:
#             login(request, user)
#             return redirect("activities/activity_list.html")

#     return render(request, "activities/login.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "ログインされました")
        else:
            messages.error(request, "ユーザー名かパスワードが違います")

    return render(request, "activities/login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "ユーザー名とパスワードを入力してください")
            return render(request, "activities/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "このユーザー名はすでに使われています")
            return render(request, "activities/signup.html")

        User.objects.create_user(username=username, password=password)

        messages.success(request, "登録が完了しました。ログインしてください")
        return redirect("login")
    
    return render(request, "activities/signup.html")


def activity_list(request):
    if request.method == "POST":
        for activity in Activity.objects.all():
            if str(activity.id) in request.POST:
                activity.is_done = True
                activity.save()

        messages.success(request, "保存しました！")

        Activity.objects.update(is_done=False)

        return redirect("activity_list")  # POST後はリダイレクト（OK）

    activities = Activity.objects.all()
    return render(request, "activities/activity_list.html", {"activities": activities})
