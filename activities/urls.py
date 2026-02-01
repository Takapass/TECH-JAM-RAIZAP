from django.urls import path
from .views import activity_list, home, group

urlpatterns = [
    path('', activity_list, name='activity_list'),
    path('home/', home, name='home'),
    path('group/', group, name='group'),
]