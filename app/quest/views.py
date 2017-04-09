from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from django.template import RequestContext
from django.template import loader
from django.views import generic

from .models import Quest, Question, Choise


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'quest/index.html'
    context_object_name = 'quest_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Quest.objects.all()


def questions(request, quest_id):
    questions = get_list_or_404(Question, quest_id=quest_id)
    return render(
        request=request,
        template_name="quest/questions.html",
        context={'questions': questions}
    )