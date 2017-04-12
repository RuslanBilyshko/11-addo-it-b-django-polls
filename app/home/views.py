from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import views

# Create your views here.
from django.urls import reverse


def index(request):
    if not request.user.is_authenticated:
        template_response = views.login(request)
        return template_response
    else:
        return HttpResponseRedirect(reverse('quest:index'))
