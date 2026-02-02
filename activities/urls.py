from django.urls import path
from .views import login_view, signup_view, activity_list, home, profile_view, group_view

urlpatterns = [
    path("", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("list/", activity_list, name="activity_list"),
    path('home/', home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('group/', group_view, name='group'),
]
