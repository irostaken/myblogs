import requests
from bs4 import BeautifulSoup

from django.views import View
from django.shortcuts import render
from django.utils.safestring import mark_safe

from blogs.models import Menu


class SupportView(View):
    def crawl(self, target_url):
        try:
            response = requests.get(target_url, timeout=3)
            soup = BeautifulSoup(response.text, features='html.parser')
            result = response.text
        except Exception as e:
            return "time out."
        return result

    def get(self, request, *args, **kwargs):
        target_url = request.GET.get("target_url")
        response_text = ''
        if target_url:
            response_text = self.crawl(target_url)
        menus = Menu.objects.all()
        cur_url = "blogs:supports"
        return render(request, 'blogs/sidebar/supports.html', {
            "menus": menus,
            "cur_url": cur_url,
            "response_text": response_text,
        })
