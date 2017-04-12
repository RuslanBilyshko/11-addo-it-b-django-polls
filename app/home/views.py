from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import views

# Create your views here.
from django.urls import reverse


def index(request):
    template_response = views.login(request)
    return template_response


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
        auth.login(request, user)
        # Перенаправление на "правильную" страницу
        return HttpResponseRedirect(reverse("quest:index"))
    else:
        # Отображение страницы с ошибкой
        return render(
            request=request,
            template_name="home/index.html",
            #context={'questions': questions, "quest": quest, "form": form, "data": rdata}
        )


def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/account/loggedout/")
