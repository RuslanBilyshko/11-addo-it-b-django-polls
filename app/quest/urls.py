from django.conf.urls import url

from . import views

app_name = 'quest'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<quest_id>[0-9]+)/$', views.questions, name='questions'),
]
