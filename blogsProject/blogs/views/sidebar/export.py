from django.views import View
from django.shortcuts import render

from blogs.models import Menu, UserProfile


class ExportView(View):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        if not request.COOKIES.get("user"):
            menus = UserProfile.objects.get(name="common").menus.all()

        cur_url = "blogs:export"
        return render(request, 'blogs/sidebar/export.html', {
            "menus": menus,
            "cur_url": cur_url
        })
