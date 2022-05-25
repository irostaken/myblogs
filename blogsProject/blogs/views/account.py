from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from blogs.models import UserProfile

import hashlib
import time


class AuthView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'blogs/login.html')

    def authenticate(self):
        response_data = {"email_error": None, 'password_error': None}
        email = self.request.POST.get("email")
        password = self.request.POST.get("password")
        response_data["email"] = email
        response_data['password'] = password
        try:
            user = UserProfile.objects.get(email=email)
            if user.password == password:
                response_data["user"] = user
            else:
                response_data["password_error"] = "Wrong Password."
        except UserProfile.DoesNotExist:
            response_data["email_error"] = "Invalid Email."
        return response_data

    def create_token(self):
        m = hashlib.md5()
        m.update(str(time.time()).encode('utf-8'))
        return m.hexdigest()

    def post(self, request, *args, **kwargs):
        response_data = self.authenticate()
        user = response_data.get("user")
        if user:
            req = redirect(reverse('blogs:index'))
            req.set_cookie("user", user)
            return req
        return render(request, 'blogs/login.html', response_data)


def logout(request):
    req = redirect(reverse('blogs:index'))
    req.delete_cookie("user")
    return req
