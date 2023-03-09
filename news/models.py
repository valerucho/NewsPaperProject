from django.db import models
from datetime import datetime
from news.resources import TYPE, news
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    # author_name = models.CharField(max_length = 255)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating_sum = self.post_set.aggregate(post_rate=Sum('post_rate'))
        p_rat = 0
        p_rat += post_rating_sum.get('post_rate')

        comment_rating_sum = self.author_user.comment_set.aggregate(comment_rate=Sum('comment_rate'))
        c_rat = 0
        c_rat += comment_rating_sum.get('comment_rate')

        self.author_rating = p_rat * 3 + c_rat
        self.save()



class Category(models.Model):
    category_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_type = models.CharField(max_length=2, choices=TYPE, default=news)
    post_name = models.CharField(max_length=255)
    post_value = models.TextField()
    post_rate = models.SmallIntegerField(default=0)

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rate += 1
        self.save()

    def dislike(self):
        self.post_rate -= 1
        self.save()

    def post_rating(self):
        return self.post_rate

    def preview(self):
        return '{}...'.format(self.post_value[:124])

    def __str__(self):
        return f'{self.post_name.title()}: {self.preview()}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_datetime = models.DateTimeField(auto_now_add=True)
    comment_rate = models.SmallIntegerField(default=0)
    comment_value = models.TextField(max_length=512)

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rate += 1
        self.save()

    def dislike(self):
        self.comment_rate -= 1
        self.save()

    def comment_rating(self):
        return self.comment_rate

