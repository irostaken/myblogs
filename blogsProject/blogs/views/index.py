import datetime

from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator

from ..models import UserProfile, Menu, Article, ArticleType


class IndexView(View):
    def filter(self):
        articles = Article.objects.all().order_by("-pub_date")
        article_type = self.request.GET.get("article_type")
        date = self.request.GET.get("date")
        article_search = self.request.GET.get("article_search")
        if article_type:
            if article_type != "All":
                articles = articles.filter(article_type__name=article_type)
        if date:
            cur_time = datetime.datetime.now()
            if date == "Today":
                articles = articles.filter(pub_date__day=str(cur_time.day))
            if date == 'Last 7 days':
                articles = articles.filter(pub_date__gte=cur_time-datetime.timedelta(days=7))
            if date == 'This month':
                articles = articles.filter(pub_date__month=str(cur_time.month))
            if date == 'This year':
                articles = articles.filter(pub_date__year=str(cur_time.year))
        if article_search:
            articles = Article.objects.filter(content__icontains=article_search)

        return articles, date, article_type

    def pager(self, articles):
        page_obj = Paginator(articles, 13)
        cur_page = self.request.GET.get("page")
        if not cur_page:
            cur_page = 1

        return page_obj.get_page(cur_page), cur_page, page_obj.num_pages

    def get(self, request, *args, **kwargs):
        articles, date, article_type = self.filter()
        articles, cur_page, total_page = self.pager(articles)
        menus = Menu.objects.all()
        if not request.COOKIES.get("user"):
            menus = UserProfile.objects.get(name="common").menus.all()
        article_types = ArticleType.objects.all()
        return render(request, 'blogs/index.html', {
            "menus": menus,
            "cur_url": "blogs:index",
            "articles": articles,
            "article_types": article_types,
            "date": date,
            "article_type": article_type,
            "cur_page": cur_page,
            "total_page": total_page,
        })
