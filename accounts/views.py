from __future__ import unicode_literals
from django.http import HttpResponse
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from accounts.forms import MazeLoginForm
from django.views.generic import View, TemplateView
from django.conf import settings


def homeview(request):
    "a home view"
    return render(request, 'index.html')

def loginview(request):
    "a login view"
    return render(request, 'allauth/account/login-existing.html')

def logoutview(request):
    "a logout view"
    return render(request, 'index.html')

def testview(request):
    "a test view"
    return render(request, 'signup.html')


class LoginView(TemplateView):
    """
      Login View for User
    """
    template_name = 'allauth/account/login.html'
    form = MazeLoginForm()
    redirect_url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            ctx = {}
            ctx['redirect_url'] = self.redirect_url
            ctx['status'] = True
            return HttpResponse(json.dumps(ctx), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': False}), content_type="application/json")