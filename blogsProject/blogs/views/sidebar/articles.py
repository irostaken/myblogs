import datetime

from django.views import View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django import forms
from django.urls import reverse

from blogs.models import Menu, Article, ArticleType, UserProfile


class ArticleView(View):
    def filter(self, article_type):
        articles = Article.objects.all()
        if article_type:
            articles = Article.objects.filter(article_type__name=article_type)
        wd = self.request.GET.get("wd")
        page = self.request.GET.get("page")
        pub_date_sort = self.request.GET.get("pub_date_sort", "0")
        if not page:
            page = 1
        if wd:
            articles = articles.filter(title__icontains=wd)
        articles = articles.order_by("-pub_date")
        if pub_date_sort == "1":
            articles = articles.order_by("pub_date")
        page_obj = Paginator(articles, 14)
        total_page = page_obj.num_pages
        return page_obj.get_page(page), total_page, page, article_type, wd, pub_date_sort

    def get(self, request, article_type=None, *args, **kwargs):
        aid = request.GET.get("aid")
        if aid:
            Article.objects.get(id=aid).delete()
            return HttpResponse("Article has been deleted successfully.")
        articles, total_page, page, article_type, wd, pub_date_sort = self.filter(article_type)
        menus = Menu.objects.all()
        article_types = ArticleType.objects.all()
        return render(request, 'blogs/sidebar/articles/list.html', {
            "articles": articles,
            "article_types": article_types,
            'cur_type': article_type,
            'cur_page': page,
            "cur_url": "blogs:articles",
            "menus": menus,
            'total_page': total_page,
            'wd': wd,
            "pub_date_sort": pub_date_sort,
        })


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['pub_date', 'owner']
        widgets = {
            'content': forms.Textarea(attrs={"id": "content"}),
        }


class AddView(View):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        form_obj = ArticleForm()
        return render(request, 'blogs/sidebar/articles/add.html', {
            'menus': menus,
            'cur_url': 'blogs:articles',
            'form_obj': form_obj,
        })

    def post(self, request, *args, **kwargs):
        form_obj = ArticleForm(request.POST)
        menus = Menu.objects.all()
        if form_obj.is_valid():
            d = datetime.datetime.now()
            Article.objects.create(owner_id=2, pub_date=d, **form_obj.cleaned_data)
            return redirect(reverse('blogs:articles'))
        select_error = ''
        if not request.POST.get("article_type"):
            select_error = "This field is required."
        return render(request, 'blogs/sidebar/articles/add.html', {
            'menus': menus,
            'cur_url': 'blogs:articles',
            "form_obj": form_obj,
            "select_error": select_error,
        })


class EditView(View):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        article_id = kwargs.get("article_id")
        article = Article.objects.get(id=article_id)
        form_obj = ArticleForm(instance=article)
        return render(request, 'blogs/sidebar/articles/edit.html', {
            'menus': menus,
            'cur_url': "blogs:articles",
            'form_obj': form_obj,
            'article_id': article_id,
        })

    def post(self, request, *args, **kwargs):
        form_obj = ArticleForm(request.POST)
        article_id = kwargs.get("article_id")
        if form_obj.is_valid():
            d = datetime.datetime.now()
            Article.objects.filter(id=article_id).update(pub_date=d, **form_obj.cleaned_data)
        return redirect(reverse("blogs:articles"))


class DetailView(View):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        cur_url = "blogs:articles"
        if not request.COOKIES.get("user"):
            menus = UserProfile.objects.get(name="common").menus.all()
            cur_url = "blogs:index"
        article_id = kwargs.get("article_id")
        article = Article.objects.get(id=article_id)
        return render(request, 'blogs/sidebar/articles/detail.html', {
            "menus": menus,
            "cur_url": cur_url,
            "article": article,
        })
