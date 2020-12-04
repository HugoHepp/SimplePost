
from django.urls import path

from . import views

urlpatterns = [

    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("following/", views.following, name="following"),
    path("send_post/", views.send_post, name="send_post"),
    path("edit_content/<int:pk>", views.edit_content, name="edit_content"),
    path("my_profile/send_post/", views.send_post, name="send_post"),   
    path("like_post/<int:pk>", views.like_post, name="like_post"),
    path("follow_user/<int:pk>", views.follow_user, name="follow_user")

]