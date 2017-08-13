from __future__ import unicode_literals
from django.http import HttpResponse
import requests
import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from accounts.forms import MazeLoginForm
from accounts.models import User
from django.views.generic import View, TemplateView
from django.conf import settings
import datetime


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


class SignUpView(TemplateView):
    """
      Signup View for User
    """
    template_name = 'signup.html'
    redirect_url = settings.LOGIN_REDIRECT_URL

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        user_exist = User.objects.filter(email__iexact=email)
        ctx = {}
        if not user_exist:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            dob = datetime.datetime.strptime(dob, "%d-%m-%Y").strftime("%Y-%m-%d")
            mobile_number = request.POST.get('mobile_number')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                """captcha verification"""
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()
                if result['success']:
                    user = User()
                    user.email = email
                    user.username = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.gender = gender
                    user.dob = dob
                    user.phone_number = mobile_number
                    user.set_password(password)
                    user.save()
                    ctx['status'] = True
                    return HttpResponse(json.dumps(ctx), content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'captcha': False}), content_type="application/json")
        else:
            ctx['status'] = False
            return HttpResponse(json.dumps({'status': False}), content_type="application/json")