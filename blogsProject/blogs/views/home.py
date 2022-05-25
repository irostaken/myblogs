from django.shortcuts import render, redirect, reverse
from django.views import View
from ..models import UserProfile


class HomeView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.COOKIES.get("user_id")
        if user_id:
            try:
                user = UserProfile.objects.get(id=user_id)
                return render(request, 'blogs/home.html', {"user_obj": user})
            except UserProfile.DoesNotExist:
                pass
        return redirect(reverse('blogs:index'))
