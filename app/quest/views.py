from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.template import loader
from django.forms import modelformset_factory
from django.views import generic
from var_dump import var_dump

from .models import Quest, Question, Choise, Choise_result
from .forms import get_form


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'quest/index.html'
    context_object_name = 'quest_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Quest.objects.all()



def questions(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    questions = get_list_or_404(Question, quest=quest)
    choises = get_list_or_404(Choise, question__in=questions)

    data_form = []

    for index, q in enumerate(questions):
        questions[index].choises = [x for x in choises if x.question_id == q.id]

    for q in questions:
        data = {
            "name": "question--{}".format(q.id),
            "label": q.question_text,
            "type": q.choise_type.type,
            "required": 1
        }

        chs = []

        if q.choises:
            for c in q.choises:
                chs.append({"name": c.choice_text, "value": c.id})

        data['choices'] = chs
        data_form.append(data)

    form_class = get_form(data_form)

    rdata = {}

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            rdata = form.cleaned_data

            objects = []

            for ch in init_data_from_choice_objects(quest_id, rdata):
                objects.append(Choise_result(**ch))

            Choise_result.objects.bulk_create(objects)

            return HttpResponseRedirect(reverse('quest:result', args=(quest_id,)))
    else:
        form = form_class()

    # AuthorFormSet = modelformset_factory(Choise, fields=('choice_text', 'id'))
    # var_dump(questions[0])


    return render(
        request=request,
        template_name="quest/questions.html",
        context={'questions': questions, "quest": quest, "form": form, "data": rdata}
    )


def init_data_from_choice_objects(quest_id, data: dict, key_separator="--"):
    result = []
    for key, item in data.items():
        question = key.split(key_separator)

        if type(item) is list:
            for it in item:
                result.append(init_data_from_choice_object(quest_id, question[1], it))
        else:
            result.append(init_data_from_choice_object(quest_id, question[1], item))
        #print(key.split(key_separator), item)

    #var_dump(result)
    return result


def init_data_from_choice_object(quest, question, choise):
    return {"quest_id": quest, "question_id": question, "choise_id": choise}


def quest_result(request, quest_id):
    quest = get_object_or_404(Quest, pk=quest_id)
    ch_result = get_list_or_404(Choise_result, quest=quest)
    var_dump(ch_result)
    return render(
        request=request,
        template_name="quest/quest_result.html",
        context={'result': ch_result, "title": quest.title}
    )


