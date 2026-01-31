from django.urls import path
from .views import login_view, signup_view, activity_list

urlpatterns = [
    path("", login_view, name="login"),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("list/", activity_list, name="activity_list"),
]
