from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html")  # ←ホーム画面のHTMLに変更する


def login_view(request):
    return render(request, "saving/login.html")


def signup_view(request):
    return render(request, "saving/signup.html")