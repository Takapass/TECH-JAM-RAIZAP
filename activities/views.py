from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Activity
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import DailyStamp
from .models import Idea

def login_view(request):
    if request.method == "POST":
        login_id = request.POST.get("login_id")
        password = request.POST.get("password")

        user = authenticate(request, username=login_id, password=password)

        if user is None:
            try:
                user_obj = User.objects.filter(email=login_id).first()
                if user_obj:
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
                request, "＊ユーザー名またはメールアドレスかパスワードが違います"
            )

    return render(request, "activities/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if not username or not password:
#             messages.error(request, "＊ユーザー名とパスワードを入力してください")
#             return render(request, "activities/signup.html")

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "＊このユーザー名はすでに使われています")
#             return render(request, "activities/signup.html")

#         User.objects.create_user(username=username, email=email, password=password)

#         messages.success(request, "登録が完了しました。ログインしてください")
#         return redirect("login")

#     return render(request, "activities/signup.html")


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

        # 👇 ユーザー作成
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # 👇【ここ】Activityをユーザー分まとめて作る
        for key, label in Activity.ACTIVITY_CHOICES:
            Activity.objects.create(
                user=user,
                activity_type=key,
                title=label
            )

        messages.success(request, "登録が完了しました。ログインしてください")
        return redirect("login")

    return render(request, "activities/signup.html")


# def activity_list(request):
#     if request.method == "POST":
#         for activity in Activity.objects.all():
#             if str(activity.id) in request.POST:
#                 activity.is_done = True
#                 activity.save()

#         messages.success(request, "保存しました！")

#         Activity.objects.update(is_done=False)

#         return redirect("activity_list")  # POST後はリダイレクト（OK）

#     # activities = Activity.objects.all()
#     activities = Activity.objects.filter(user=request.user)
#     return render(request, "activities/home.html", {"activities": activities})


@login_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user)

    if request.method == "POST":
        for activity in activities:
            activity.is_done = str(activity.id) in request.POST
            activity.save()

        messages.success(request, "保存しました！")
        return redirect("activity_list")

    return render(request, "activities/home.html", {"activities": activities})


@login_required
def create_activity(request):
    if request.method == "POST":
        activity_type = request.POST.get("activity_type")

        Activity.objects.create(
            activity_type=activity_type,
            user=request.user,   # ← ★ ここが超重要
        )

        return redirect("activity_list")


@login_required
def home(request):
    stamp, _ = DailyStamp.objects.get_or_create(user=request.user)

    context = {
        "total_days": stamp.total_days,
        "can_stamp": stamp.can_stamp_today(),
        "max_stamps": range(5),   # ← ★ ここを追加
    }
    return render(request, "activities/home.html", context)


@login_required(login_url="login")
def profile_view(request):
    user = request.user
    activities = Activity.objects.filter(user=request.user)
    # activities = Activity.objects.all()
    completed_count = activities.filter(is_done=True).count()
    total_activities = activities.count()

    context = {
        "user": user,
        "completed_count": completed_count,
        'total_activities': total_activities,
        # 当面は0を返す。将来的にユーザーの連続日数ロジックに置き換える
        'streak_days': 0,
    }
    return render(request, "activities/profile.html", context)


@login_required(login_url="login")
def group_view(request):
    return render(request, "activities/group.html")


@login_required(login_url="login")
def idea_view(request):
    return render(request, "activities/idea.html")


@login_required
def stamp_done(request):
    stamp, created = DailyStamp.objects.get_or_create(user=request.user)
    today = timezone.localdate()

    if stamp.last_stamped_date == today:
        return redirect("home")  # 今日はもう押せない

    stamp.last_stamped_date = today
    stamp.total_days += 1
    stamp.save()

    return redirect("home")


@login_required
def stamp_skip(request):
    stamp, _ = DailyStamp.objects.get_or_create(user=request.user)
    today = timezone.localdate()

    # 今日すでに「できた」or「パス」してたら何もしない
    if stamp.last_stamped_date == today or stamp.last_skipped_date == today:
        return redirect("home")

    stamp.last_skipped_date = today
    stamp.save()

    return redirect("home")





@login_required
def idea_view(request):
    if request.method == 'POST':
        Idea.objects.create(
            user=request.user,
            content=request.POST['content']
        )
        return redirect('idea')

    ideas = Idea.objects.all().order_by('-created_at')
    return render(request, 'activities/idea.html', {
        'ideas': ideas
    })