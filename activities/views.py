from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        login_id = request.POST.get("login_id")
        password = request.POST.get("password")

        user = authenticate(request, username=login_id, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(email=login_id)
                user = authenticate(
                    request, username=user_obj.username, password=password
                )
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("activity_list")
        else:
            messages.error(
                request, "*ユーザー名またはメールアドレスかパスワードが違います"
            )

    return render(request, "activities/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(request, "＊ユーザー名とパスワードを入力してください")
            return render(request, "activities/signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "＊このユーザー名はすでに使われています")
            return render(request, "activities/signup.html")

        User.objects.create_user(username=username, email=email, password=password)

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
    return render(request, "activities/home.html", {"activities": activities})


def home(request):
    activities = Activity.objects.all()
    return render(request, "activities/home.html", {"activities": activities})


@login_required(login_url="login")
def profile_view(request):
    user = request.user
    activities = Activity.objects.all()
    completed_count = activities.filter(is_done=True).count()
    total_activities = activities.count()

    context = {
        "user": user,
        "completed_count": completed_count,
        "total_activities": total_activities,
    }
    return render(request, "activities/profile.html", context)


@login_required(login_url="login")
def group_view(request):
    return render(request, "activities/group.html")