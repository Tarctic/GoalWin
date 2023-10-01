from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_group", views.create_group, name="create_group"),
    path("create_goal", views.create_goal, name="create_goal"),
    path("join_group/<str:joining_group>/", views.join_group, name="join_group"),
    path("goal_completed", views.goal_completed, name="goal_completed"),
]
