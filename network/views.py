from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Post, Follow, Like
from django.core.paginator import Paginator
import datetime
import json
from django.http import JsonResponse


# FORM TO MAKE A POST
class Post_form(forms.Form):

    content = forms.CharField(max_length=255, label='', widget=forms.Textarea(attrs={'class' : 'postform_content', 'style': 'padding:10px;'}))

def index(request):

    # get general newsfeed
    posts_list = Post.objects.all().order_by("date").reverse()

    # if user is logged dipslay the post form 
    if request.user.is_authenticated:
        form = Post_form()
        paginator = Paginator(posts_list, 10)
        likes_of_user = Like.objects.filter(user_who_liked=request.user).values_list('liked_post__id', flat=True)
        page = request.GET.get('page')
        post = paginator.get_page(page)
        return render(request, "network/index.html", {"post":post, "form":form, "likes_of_user":likes_of_user})
    else:
        paginator = Paginator(posts_list, 10) 
        page = request.GET.get('page')
        post = paginator.get_page(page)
        return render(request, "network/index.html", {"post":post})


def profile(request, pk):

    # if user visits his profile he will be redirected to my_profile
    if pk == request.user.id:
        return HttpResponseRedirect(reverse("my_profile")) 

    # get newsfeed by author
    posts_list = Post.objects.filter(author=pk) 
    # paginate
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    post = paginator.get_page(page)
    # get likes of user logged
    likes_of_user = Like.objects.filter(user_who_liked=request.user).values_list('liked_post__id', flat=True)
    # get follows of user logged
    follows_of_user = Follow.objects.filter(follower=request.user).values_list('followed__id', flat=True)
    # get count of followers of user 
    followers = Follow.objects.filter(followed = pk).count()
    following = Follow.objects.filter(follower = pk).count()
    # get username of profile
    user_profile = User.objects.get(id=pk)
    username_profile = user_profile.username
    # return template
    return render(request, "network/profile.html", {"post":post,'username_profile':username_profile, 'followers':followers, 'following':following, "follows_of_user":follows_of_user, "likes_of_user":likes_of_user, "user_id":pk})


def my_profile(request):

    # get newsfeed of user logged
    posts_list = Post.objects.filter(author=request.user.id) 
    # paginate
    paginator = Paginator(posts_list, 10) 
    page = request.GET.get('page')
    post = paginator.get_page(page)
    # create form to post
    form = Post_form()
    # get likes of user logged
    likes_of_user = Like.objects.filter(user_who_liked=request.user).values_list('liked_post__id', flat=True)
    # get follows of user logged
    follows_of_user = Follow.objects.filter(follower=request.user).values_list('followed__id', flat=True)
    # get count of follows and followers 
    followers = Follow.objects.filter(followed = request.user).count()
    following = Follow.objects.filter(follower = request.user).count()
    # render template
    return render(request, "network/my_profile.html", {"post":post,"form":form, 'followers':followers, 'following':following,"follows_of_user":follows_of_user, "likes_of_user":likes_of_user})


def following(request):

    # get queryset of follows of user logged
    following_user_list = Follow.objects.filter(follower = request.user.id)
    # create list of following
    list_following = []
    for follow_user in following_user_list :
        list_following.append(follow_user.followed.id)
    list_following = list(map(int, list_following))
    # get list of posts of users in the list of following 
    posts_list = Post.objects.filter(author__in = list_following).order_by("date").reverse()
    # paginate
    paginator = Paginator(posts_list, 10) 
    page = request.GET.get('page')
    post = paginator.get_page(page)
    # get list of likes of user logged 
    likes_of_user = Like.objects.filter(user_who_liked=request.user).values_list('liked_post__id', flat=True)
    # render template
    return render(request, "network/following.html", {"post":post, "likes_of_user":likes_of_user})

#=========== API =====================================#

def like_post(request, pk):
    # get post object liked 
    liked_post = Post.objects.get(id=pk)
    # get user logged 
    user_who_liked = User.objects.get(id=request.user.id)
    # get author of the post 
    post_author = liked_post.author
    # check if the post is already liked 
    if Like.objects.filter(liked_post=liked_post, user_who_liked=user_who_liked, post_author=post_author):
        # remove like from database
        Like.objects.get(liked_post=liked_post, user_who_liked=user_who_liked, post_author=post_author).delete()
        # remove like from counter 
        liked_post.likes_num = liked_post.likes_num - 1;
        liked_post.save()
        # return 
        return JsonResponse("unliked", safe=False)
    # if not already liked 
    else:
        # create like object and save
        newlike = Like(liked_post=liked_post, user_who_liked=user_who_liked, post_author=post_author)
        newlike.save()
        # add like to counter
        liked_post.likes_num = liked_post.likes_num + 1;
        liked_post.save()
        # return
        return JsonResponse("liked", safe=False)


def follow_user(request, pk):
    # get user followed
    followed = User.objects.get(id=pk)
    # get user logged
    follower = User.objects.get(id=request.user.id)
    # check if user is already followed
    if Follow.objects.filter(followed=followed, follower=follower):
        # delete follow
        Follow.objects.filter(followed=followed, follower=follower).delete()
        # update counter of follow
        followed.followers_num = followed.followers_num - 1;
        followed.save()
        follower.following_num = follower.following_num - 1
        follower.save()
        return JsonResponse("unfollowed" ,safe=False)
    else:
        # create follow
        follow = Follow(followed=followed, follower=follower)
        follow.save()
        # update counter of follow
        followed.followers_num = followed.followers_num + 1
        followed.save()
        follower.following_num = follower.following_num + 1
        follower.save()
        # return 
        return JsonResponse("followed" ,safe=False)

def edit_content(request, pk):


    # check if method is POST 
    if request.method != "POST":
        return HttpResponse("POST request required.", status=400) 

    # get data from fetch 
    data = json.loads(request.body);
    # prepare field to update
    content = data.get("content", "")
    date = datetime.datetime.now()
    # get original post 
    original_post = Post.objects.get(id=pk)

    # if the userlogged different to the author of the original post
    if original_post.author != request.user:
        return HttpResponse("Error, not allowed", status=400)

    # update fields
    original_post.author = request.user
    original_post.date = date
    original_post.content = content
    original_post.save()
    return HttpResponse("saved")

def send_post(request):

    # check if method is POST 
    if request.method != "POST":
        return HttpResponse("POST request required.", status=400)
    # Load data from django form
    form = Post_form(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # Clear and save post
        content = form.cleaned_data['content']
        date= datetime.datetime.now()
        author = request.user
        newpost = Post(author = author, content = content, date = date,likes_num=0)
        newpost.save()
    return HttpResponseRedirect(reverse('index'))
    













































def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
