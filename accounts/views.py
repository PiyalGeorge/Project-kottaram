from __future__ import unicode_literals

from django.shortcuts import render



def homeview(request):
    "a home view"
    return render(request, 'index.html')

def loginview(request):
    "a login view"
    return render(request, 'allauth/account/login.html')

def logoutview(request):
    "a logout view"
    return render(request, 'index.html')