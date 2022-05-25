from django.db import models


# Create your models here.

class UserProfile(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    menus = models.ManyToManyField("Menu")

    def __str__(self):
        return self.name


class Menu(models.Model):
    name = models.CharField(max_length=128)
    url = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class ArticleType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=128)
    summary = models.CharField(max_length=128, blank=True)
    content = models.TextField()
    pub_date = models.DateTimeField()

    owner = models.ForeignKey("UserProfile", on_delete=models.CASCADE)

    article_type = models.ForeignKey("ArticleType", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
