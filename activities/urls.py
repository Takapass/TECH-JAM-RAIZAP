from django.urls import path
from .views import login_view, signup_view, activity_list, home, profile_view, group_view, idea_view, delete_idea, react_idea
from . import views

urlpatterns = [
    path("", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("list/", activity_list, name="activity_list"),
    path('home/', home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('group/', group_view, name='group'),
    path('ideas/', idea_view, name='idea'),
    path("stamp/", views.stamp_done, name="stamp_done"),
    path("stamp/skip/", views.stamp_skip, name="stamp_skip"),
    path('ideas/<int:idea_id>/delete/', delete_idea, name='delete_idea'),
    path('ideas/<int:idea_id>/react/<str:reaction_type>/', react_idea, name='react_idea'),
    path("change_email/", views.change_email, name="change_email"),
    path("change_password/", views.change_password, name="change_password"),
]
