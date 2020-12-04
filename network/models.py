from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

	followers_num = models.SmallIntegerField(default=0)
	following_num = models.SmallIntegerField(default=0)

class Post(models.Model):

	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "author")
	content = models.CharField(max_length=255)
	date = models.DateTimeField()
	likes_num = models.SmallIntegerField(default=0)

class Follow(models.Model):

	follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
	followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followed")
	

class Like(models.Model):

	post_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_owner")
	liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
	user_who_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")

