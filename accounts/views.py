from __future__ import unicode_literals

from django.shortcuts import render

def testview(request):
    "a simple view"
    return render(request, 'simple.html')